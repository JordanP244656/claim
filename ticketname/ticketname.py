import discord
from discord.ext import commands
from core.models import getLogger

logger = getLogger(__name__)


class TicketName(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    def get_next_ticket_number(self, guild):

        highest = 0

        for channel in guild.text_channels:

            name = channel.name

            # Only consider channels that are pure numbers
            if name.isdigit():

                num = int(name)

                if num > highest:
                    highest = num

        return highest + 1


    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:

            guild = thread.channel.guild

            next_number = self.get_next_ticket_number(guild)

            ticket_id = f"{next_number:03}"

            await thread.channel.edit(name=ticket_id)

        except discord.errors.Forbidden:
            logger.error("Missing permission to rename ticket channel.")

        except Exception as e:
            logger.error(f"TicketName error: {e}")


async def setup(bot):
    await bot.add_cog(TicketName(bot))