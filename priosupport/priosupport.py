import discord
from discord.ext import commands
from discord.ext.commands.view import StringView
import asyncio
import copy

from core.models import getLogger, DummyMessage

logger = getLogger(__name__)

PRIORITY_CATEGORY_ID = 1482559663756017716


STAFF_PING = "<@698506622263230497>"
MESSAGE = "🚨 Priority support ticket opened. Staff have been notified."


class PriorityMessage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread):

        try:

            channel = thread.channel

            if not channel or channel.category_id != PRIORITY_CATEGORY_ID:
                return

            # wait for modmail thread setup
            await asyncio.sleep(4)

            # message inside ticket
            await channel.send(f"{STAFF_PING} {MESSAGE}")

            # send DM to user through modmail
            await thread.reply(
                message=MESSAGE,
                anonymous=False
            )

        except Exception as e:
            logger.error(f"Priority plugin error: {e}")


async def setup(bot):
    await bot.add_cog(PriorityMessage(bot))