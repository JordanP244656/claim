import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)

PRIORITY_EMOJI = "⭐"
TARGET_MESSAGE_ID = 1482883082217586831
PRIORITY_CATEGORY_ID = 1088928972592644116
STAFF_ROLE_ID = 123456789012345678

class PrioritySupport(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.user_id == self.bot.user.id:
            return

        if payload.message_id != TARGET_MESSAGE_ID:
            return

        if str(payload.emoji) != PRIORITY_EMOJI:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        user = guild.get_member(payload.user_id)
        if not user:
            return

        try:

            # BYPASS THREADMENU
            thread = await self.bot.threads.create(
                recipient=user,
                manual_trigger=True
            )

            if not thread:
                return

            channel = thread.channel

            category = guild.get_channel(PRIORITY_CATEGORY_ID)
            if category:
                await channel.edit(category=category)

            await channel.send(
                f"<@&{STAFF_ROLE_ID}> 🚨 **Priority Support Ticket**\n"
                f"Opened by {user.mention}"
            )

        except Exception as e:
            logger.error(f"Priority ticket error: {e}")

        # remove ONLY the user's reaction so they can click again later
        try:
            reaction_channel = self.bot.get_channel(payload.channel_id)
            message = await reaction_channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, user)
        except Exception:
            pass


async def setup(bot):
    await bot.add_cog(PrioritySupport(bot))