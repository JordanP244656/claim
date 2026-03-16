import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)


class TicketNumbers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def next_ticket(self):

        config = await self.bot.config.all()

        number = config.get("ticket_counter", 0) + 1

        await self.bot.config.update({"ticket_counter": number})

        return number


    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:

            number = await self.next_ticket()

            ticket_id = f"{number:03}"

            # rename channel
            await thread.channel.edit(
                name=f"ticket-{ticket_id}"
            )

            embed = discord.Embed(
                title=f"Ticket #{ticket_id}",
                description=f"This ticket has been assigned ID **#{ticket_id}**.",
                color=discord.Color.blurple()
            )

            await thread.channel.send(embed=embed)

        except Exception as e:
            logger.error(f"TicketNumbers error: {e}")


async def setup(bot):
    await bot.add_cog(TicketNumbers(bot))