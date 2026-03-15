import discord
from discord.ext import commands
import asyncio

from core.models import getLogger

logger = getLogger(__name__)

PRIORITY_CATEGORY_ID = 1482559663756017716

STAFF_PING = "<@698506622263230497>"
MESSAGE = "🚨 Priority support ticket opened. Staff have been notified."


class PrioSupport(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:

            # only run for priority category
            if not category or category.id != PRIORITY_CATEGORY_ID:
                return

            # small delay so modmail finishes setup
            await asyncio.sleep(2)

            # send message in ticket
            await thread.channel.send(f"{STAFF_PING} {MESSAGE}")

            # DM the user
            await thread.recipient.send(MESSAGE)

        except Exception as e:
            logger.error(f"Priority plugin error: {e}")


async def setup(bot):
    await bot.add_cog(PrioSupport(bot))