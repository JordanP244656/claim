import discord
from discord.ext import commands
import asyncio

from core.models import getLogger

logger = getLogger(__name__)

PRIORITY_CATEGORY_ID = 1482559663756017716

STAFF_PING = "<@&1179699660181475338>"


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
                    "A membeimport discord
from discord.ext import commands
import asyncio

from core.models import getLogger, PermissionLevel
from core import checks

logger = getLogger(__name__)


class PrioSupport(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def get_config(self):
        return {
            "category": await self.bot.config.get("priority_category"),
            "staff_role": await self.bot.config.get("priority_staff_role"),
            "staff_msg": await self.bot.config.get("priority_staff_msg"),
            "user_msg": await self.bot.config.get("priority_user_msg"),
        }


    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):

        try:

            config = await self.get_config()

            if not config["category"]:
                return

            if not category or category.id != int(config["category"]):
                return

            await asyncio.sleep(2)

            role_ping = f"<@&{config['staff_role']}>" if config["staff_role"] else ""

            staff_embed = discord.Embed(
                title="Priority Support Ticket",
                description=config["staff_msg"] or f"A priority ticket has been opened by {thread.recipient.mention}.",
                color=discord.Color.red()
            )

            await thread.channel.send(content=role_ping, embed=staff_embed)

            user_embed = discord.Embed(
                title="Priority Support Ticket",
                description=config["user_msg"] or "Your priority ticket has been received.",
                color=discord.Color.blue()
            )

            await thread.recipient.send(embed=user_embed)

        except Exception as e:
            logger.error(f"Priority plugin error: {e}")


    # COMMAND GROUP
    @commands.group(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def priority(self, ctx):
        await ctx.send("Priority configuration commands.")


    # SET CATEGORY
    @priority.command()
    async def category(self, ctx, category: discord.CategoryChannel):
        await self.bot.config.set("priority_category", category.id)
        await ctx.send(f"Priority category set to **{category.name}**")


    # SET STAFF ROLE
    @priority.command()
    async def staff(self, ctx, role: discord.Role):
        await self.bot.config.set("priority_staff_role", role.id)
        await ctx.send(f"Priority staff role set to {role.mention}")


    # SET STAFF MESSSAGE
    @priority.command()
    async def staffmsg(self, ctx, *, message):
        await self.bot.config.set("priority_staff_msg", message)
        await ctx.send("Priority staff message updated.")


    # SET USER MESSAGE
    @priority.command()
    async def usermsg(self, ctx, *, message):
        await self.bot.config.set("priority_user_msg", message)
        await ctx.send("Priority user message updated.")


async def setup(bot):
    await bot.add_cog(PrioSupport(bot))r of our support team will assist you shortly.\n\n"
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