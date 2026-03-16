import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)


class TicketName(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def next_ticket(self):
        try:

            config = await self.bot.config.all()

            number = config.get("ticket_counter")

            if number is None:
                number = 0

            number += 1

            await self.bot.config.update({"ticket_counter": number})

            return number

        except Exception as e:
            logger.error(f"Ticket counter error: {e}")
            return None


    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:

            number = await self.next_ticket()

            if number is None:
                return

            ticket_id = f"{number:03}"

            # Rename channel
            await thread.channel.edit(
                name=f"ticket-{ticket_id}"
            )

            # Send embed
            embed = discord.Embed(
                title=f"Support Ticket #{ticket_id}",
                description=f"Ticket ID: **#{ticket_id}**",
                color=discord.Color.blurple()
            )

            embed.set_footer(text="ImageWorks Support System")

            await thread.channel.send(embed=embed)

        except Exception as e:
            logger.error(f"TicketName error: {e}")


async def setup(bot):
    await bot.add_cog(TicketName(bot))