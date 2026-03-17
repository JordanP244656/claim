import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)

CUSTOM_EMOJI_ID = 1310111960741707836
EMOJI_NAME = "IW_Cross"


class CloseReactionEverywhere(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔹 Add to FIRST message (genesis)
    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):
        try:
            msg = await thread.get_genesis_message()
            if msg:
                emoji = discord.PartialEmoji(name=EMOJI_NAME, id=CUSTOM_EMOJI_ID)
                await msg.add_reaction(emoji)
        except Exception as e:
            logger.warning(f"[CloseReaction] Genesis failed: {e}")

    # 🔹 Add to EVERY reply (including snippets)
    @commands.Cog.listener()
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):
        if not from_mod:
            return

        try:
            user = thread.recipient
            dm = user.dm_channel or await user.create_dm()

            emoji = discord.PartialEmoji(name=EMOJI_NAME, id=CUSTOM_EMOJI_ID)

            # 🔥 ONLY react to messages JUST sent (no scanning spam)
            async for msg in dm.history(limit=3):
                if msg.author.id == self.bot.user.id:
                    try:
                        await msg.add_reaction(emoji)
                    except:
                        pass

        except Exception as e:
            logger.warning(f"[CloseReaction] Reply failed: {e}")


async def setup(bot):
    await bot.add_cog(CloseReactionEverywhere(bot))