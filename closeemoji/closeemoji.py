import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)

CUSTOM_EMOJI_ID = 1310111960741707836
EMOJI_NAME = "IW_Cross"


class CloseReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔹 Add reaction to ALL outgoing messages (snippet safe)
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
                    except discord.NotFound:
                        continue
                    except Exception as e:
                        logger.warning(f"[CloseReaction] Reaction error: {e}")

        except Exception as e:
            logger.warning(f"[CloseReaction] Failed to add reaction: {e}")

    # 🔹 CORRECT reaction handler
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.emoji.id != CUSTOM_EMOJI_ID:
            return

        # must be DM
        if payload.guild_id is not None:
            return

        if payload.user_id == self.bot.user.id:
            return

        try:
            # 🔥 THIS IS THE KEY FIX
            thread = await self.bot.threads.find_by_message(payload.message_id)

        except Exception as e:
            logger.error(f"[CloseReaction] Thread lookup failed: {e}")
            return

        if thread is None or thread.closed:
            return

        user = self.bot.get_user(payload.user_id)

        try:
            await thread.close(
                closer=user,
                message="User closed the ticket.",
                silent=False
            )
        except Exception as e:
            logger.error(f"[CloseReaction] Failed to close thread: {e}")


async def setup(bot):
    await bot.add_cog(CloseReaction(bot))