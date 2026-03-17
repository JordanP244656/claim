import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)

# 🔧 YOUR EMOJI
CUSTOM_EMOJI_ID = 1310111960741707836
EMOJI_NAME = "IW_Cross"

class CloseReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):
        if not from_mod:
            return

        try:
            emoji = discord.PartialEmoji(name=EMOJI_NAME, id=CUSTOM_EMOJI_ID)
            await message.add_reaction(emoji)
        except Exception as e:
            logger.warning(f"[CloseReaction] Failed to add reaction: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        # ✅ Only your custom emoji
        if payload.emoji.id != CUSTOM_EMOJI_ID:
            return

        # ✅ Must be DM (user side)
        if payload.guild_id is not None:
            return

        user = self.bot.get_user(payload.user_id)
        if user is None or user.bot:
            return

        # ✅ Find thread
        thread = await self.bot.threads.find(user.id)
        if thread is None:
            return

        # ✅ Prevent double close
        if thread.closed:
            return

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