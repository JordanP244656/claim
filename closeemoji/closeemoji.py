import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)

CUSTOM_EMOJI_ID = 1310111960741707836
EMOJI_NAME = "IW_Cross"


class CloseReactionEverywhere(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔹 Genesis message
    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):
        try:
            msg = await thread.get_genesis_message()
            if msg and self.is_valid_modmail_message(msg):
                emoji = discord.PartialEmoji(name=EMOJI_NAME, id=CUSTOM_EMOJI_ID)
                await msg.add_reaction(emoji)
        except Exception as e:
            logger.warning(f"[CloseReaction] Genesis failed: {e}")

    # 🔹 Replies (snippet safe + filtered)
    @commands.Cog.listener()
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):
        if not from_mod:
            return

        try:
            user = thread.recipient
            dm = user.dm_channel or await user.create_dm()

            emoji = discord.PartialEmoji(name=EMOJI_NAME, id=CUSTOM_EMOJI_ID)

            async for msg in dm.history(limit=5):
                if msg.author.id != self.bot.user.id:
                    continue

                if not self.is_valid_modmail_message(msg):
                    continue  # 🔥 skip bad messages

                try:
                    await msg.add_reaction(emoji)
                except:
                    pass

        except Exception as e:
            logger.warning(f"[CloseReaction] Reply failed: {e}")

    # 🔥 FILTER FUNCTION (THIS FIXES YOUR ERROR)
    def is_valid_modmail_message(self, msg: discord.Message):
        if not msg.embeds:
            return False

        embed = msg.embeds[0]

        # MUST have author + URL (this is the joint ID system)
        if not embed.author or not embed.author.url:
            return False

        # MUST be sent by bot
        if msg.author.id != self.bot.user.id:
            return False

        return True


async def setup(bot):
    await bot.add_cog(CloseReactionEverywhere(bot))