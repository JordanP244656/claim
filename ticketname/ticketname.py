import discord
from discord.ext import commands
from core.models import getLogger

logger = getLogger(__name__)


class TicketName(commands.Cog):

    counter = 0

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:
            TicketName.counter += 1

            ticket_id = f"{TicketName.counter:03}"

            await thread.channel.edit(name=ticket_id)

        except discord.errors.Forbidden:
            logger.error("Missing permission to rename ticket channel.")

        except Exception as e:
            logger.error(f"TicketName error: {e}")


async def setup(bot):
    await bot.add_cog(TicketName(bot))