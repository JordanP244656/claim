import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)

CUSTOM_EMOJI_ID = 1310111960741707836
EMOJI_NAME = "IW_Cross"


class CloseReactionLatest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔹 Genesis message (first message)
    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):
        await self.update_close_reaction(thread)

    # 🔹 Every reply (handles snippets too)
    @commands.Cog.listener()
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):
        if not from_mod:
            return
        await self.update_close_reaction(thread)

    # 🔥 Core logic
    async def update_close_reaction(self, thread):
        try:
            user = thread.recipient
            dm = user.dm_channel or await user.create_dm()

            emoji = discord.PartialEmoji(name=EMOJI_NAME, id=CUSTOM_EMOJI_ID)

            latest_valid = None

            # 🔍 Find newest VALID Modmail message
            async for msg in dm.history(limit=10):
                if msg.author.id != self.bot.user.id:
                    continue

                if not msg.embeds:
                    continue

                embed = msg.embeds[0]

                # MUST be real Modmail relay message
                if not embed.author or not embed.author.url:
                    continue

                latest_valid = msg
                break

            if not latest_valid:
                return

            # 🧼 Remove reactions from older messages
            async for msg in dm.history(limit=10):
                if msg.id == latest_valid.id:
                    continue

                try:
                    await msg.clear_reactions()
                except:
                    pass

            # ➕ Add reaction to latest
            try:
                await latest_valid.add_reaction(emoji)
            except discord.HTTPException:
                pass

        except Exception as e:
            logger.warning(f"[CloseReaction] Failed: {e}")


async def setup(bot):
    await bot.add_cog(CloseReactionLatest(bot))