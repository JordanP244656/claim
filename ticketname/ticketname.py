import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)


class TicketName(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def get_next_ticket(self):

        number = await self.bot.config.get("ticket_counter", 0)

        number += 1

        await self.bot.config.set("ticket_counter", number)

        return number


    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:

            number = await self.get_next_ticket()

            ticket_id = f"{number:03}"

            # rename the ticket channel
            await thread.channel.edit(name=ticket_id)

        except Exception as e:
            logger.error(f"TicketName error: {e}")


async def setup(bot):
    await bot.add_cog(TicketName(bot))