import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)


class TicketName(commands.Cog):
    """Automatically assigns ticket numbers to channels"""

    def __init__(self, bot):
        self.bot = bot


    async def get_next_ticket(self):
        try:
            current = await self.bot.config.get("ticket_counter")
        except:
            current = None

        if not isinstance(current, int):
            current = 0

        current += 1

        await self.bot.config.set("ticket_counter", current)

        return current


    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:

            number = await self.get_next_ticket()

            ticket_id = f"{number:03}"

            # rename channel (same style as your rename command)
            await thread.channel.edit(name=ticket_id)

        except discord.errors.Forbidden:
            logger.error("Missing permissions to rename ticket channel.")

        except Exception as e:
            logger.error(f"TicketName error: {e}")


async def setup(bot):
    await bot.add_cog(TicketName(bot))