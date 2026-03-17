import discord
from discord.ext import commands
from core.models import getLogger

logger = getLogger(__name__)


class TicketName(commands.Cog):

    counter = None

    def __init__(self, bot):
        self.bot = bot


    async def initialize_counter(self, guild):
        highest = 0

        for channel in guild.text_channels:
            name = channel.name
            if name.isdigit():
                num = int(name)
                if num > highest:
                    highest = num

        TicketName.counter = highest


    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:
            guild = thread.channel.guild

            # initialize counter once
            if TicketName.counter is None:
                await self.initialize_counter(guild)

            TicketName.counter += 1

            ticket_id = f"{TicketName.counter:03}"

            await thread.channel.edit(name=ticket_id)

        except discord.errors.Forbidden:
            logger.error("Missing permission to rename ticket channel.")

        except Exception as e:
            logger.error(f"TicketName error: {e}")


async def setup(bot):
    await bot.add_cog(TicketName(bot))