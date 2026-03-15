import discord
from discord.ext import commands
import asyncio

from core.models import getLogger

logger = getLogger(__name__)

PRIORITY_CATEGORY_ID = 1482559663756017716

STAFF_PING = "<@698506622263230497>"


class PrioSupport(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:

            if not category or category.id != PRIORITY_CATEGORY_ID:
                return

            await asyncio.sleep(2)

            # STAFF EMBED (ticket channel)
            staff_embed = discord.Embed(
                title="Priority Support Ticket",
                description=(
                    f"A **priority ticket** has been opened by {thread.recipient.mention}.\n\n"
                    "Staff should respond as soon as possible."
                ),
                color=discord.Color.red()
            )

            staff_embed.set_footer(text="ImageWorks Support System")

            await thread.channel.send(
                content=STAFF_PING,
                embed=staff_embed
            )

            # USER EMBED (DM)
            user_embed = discord.Embed(
                title="Priority Support Ticket Opened",
                description=(
                    "Your **priority support ticket** has been received.\n\n"
                    "A member of our support team will assist you shortly.\n\n"
                    "Please provide us with as much detail as possible about your issue to help us resolve it quickly."
                ),
                color=discord.Color.blue()
            )

            user_embed.set_footer(text="ImageWorks Support")

            await thread.recipient.send(embed=user_embed)

        except Exception as e:
            logger.error(f"Priority plugin error: {e}")


async def setup(bot):
    await bot.add_cog(PrioSupport(bot))