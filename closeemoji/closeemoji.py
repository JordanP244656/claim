import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)

CUSTOM_EMOJI_ID = 1310111960741707836
EMOJI_NAME = "IW_Cross"


class CloseReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔹 Add reaction (unchanged, works fine)
    @commands.Cog.listener()
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):
        if not from_mod:
            return

        try:
            user = thread.recipient
            dm = user.dm_channel or await user.create_dm()

            async for msg in dm.history(limit=5):
                if msg.author.id == self.bot.user.id:
                    try:
                        emoji = discord.PartialEmoji(name=EMOJI_NAME, id=CUSTOM_EMOJI_ID)
                        await msg.add_reaction(emoji)
                    except:
                        pass

        except Exception as e:
            logger.warning(f"[CloseReaction] Failed to add reaction: {e}")

    # 🔹 PROPER CLOSE HANDLER (THIS IS THE FIX)
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.emoji.id != CUSTOM_EMOJI_ID:
            return

        if payload.guild_id is not None:
            return

        if payload.user_id == self.bot.user.id:
            return

        user = self.bot.get_user(payload.user_id)
        if not user:
            return

        try:
            # ✅ get thread (this works in your version)
            thread = await self.bot.threads.get(user.id)

            if not thread or thread.closed:
                return

            # 🔥 THIS IS THE IMPORTANT PART
            # Validate that this message belongs to THIS thread
            channel = user.dm_channel or await user.create_dm()
            message = await channel.fetch_message(payload.message_id)

            try:
                await thread.find_linked_message_from_dm(message)
            except:
                # ❌ Not part of this thread → ignore
                return

            # ✅ Now we KNOW it's correct → close
            await thread.close(
                closer=user,
                message="User closed the ticket.",
                silent=False
            )

        except Exception as e:
            logger.error(f"[CloseReaction] Close failed: {e}")


async def setup(bot):
    await bot.add_cog(CloseReaction(bot))