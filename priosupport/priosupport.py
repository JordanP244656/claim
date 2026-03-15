import discord
from discord.ext import commands
from discord.ext.commands.view import StringView
import asyncio
import copy

from core.models import getLogger, DummyMessage

logger = getLogger(__name__)

PRIORITY_CATEGORY_ID = 1482559663756017716

STAFF_PING = "<@698506622263230497>"
USER_MESSAGE = "🚨 Priority support ticket opened. Staff have been notified."


class PriorityMessage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread):

        try:

            channel = thread.channel

            if channel.category_id != PRIORITY_CATEGORY_ID:
                return

            # wait 4 seconds
            await asyncio.sleep(4)

            # send message in ticket channel
            await channel.send(f"{STAFF_PING} {USER_MESSAGE}")

            # create internal reply (user sees it)
            command = f"reply {USER_MESSAGE}"

            view = StringView(self.bot.prefix + command)

            synthetic = DummyMessage(copy.copy(thread._genesis_message))

            synthetic.author = (
                self.bot.modmail_guild.me or self.bot.user
            )

            ctx = await self.bot.get_context(synthetic)

            ctx.thread = thread
            ctx.view = view

            await self.bot.invoke(ctx)

        except Exception as e:
            logger.error(f"Priority plugin error: {e}")


async def setup(bot):
    await bot.add_cog(PriorityMessage(bot))