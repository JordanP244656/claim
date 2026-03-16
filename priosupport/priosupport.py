import discord
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

            priority_category = config["category"]

            if not priority_category:
                return

            if not category or category.id != int(priority_category):
                return

            await asyncio.sleep(2)

            staff_role = config["staff_role"]
            staff_msg = config["staff_msg"]
            user_msg = config["user_msg"]

            role_ping = f"<@&{staff_role}>" if staff_role else ""

            staff_embed = discord.Embed(
                title="Priority Support Ticket",
                description=staff_msg or f"A **priority ticket** has been opened by {thread.recipient.mention}. Staff should respond quickly.",
                color=discord.Color.red()
            )

            staff_embed.set_footer(text="ImageWorks Support System")

            await thread.channel.send(
                content=role_ping,
                embed=staff_embed
            )

            user_embed = discord.Embed(
                title="Priority Support Ticket Opened",
                description=user_msg or "Your **priority support ticket** has been received. A staff member will assist you shortly.",
                color=discord.Color.blue()
            )

            user_embed.set_footer(text="ImageWorks Support")

            await thread.recipient.send(embed=user_embed)

        except Exception as e:
            logger.error(f"Priority plugin error: {e}")


    # COMMAND GROUP
    @commands.group(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def priority(self, ctx):
        await ctx.send(
            "Priority configuration commands:\n"
            "`?priority category <category>`\n"
            "`?priority staff <role>`\n"
            "`?priority staffmsg <message>`\n"
            "`?priority usermsg <message>`"
        )


    # SET PRIORITY CATEGORY
    @priority.command()
    async def category(self, ctx, category: discord.CategoryChannel):

        await self.bot.config.set("priority_category", category.id)

        await ctx.send(
            f"Priority category set to **{category.name}**"
        )


    # SET STAFF ROLE
    @priority.command()
    async def staff(self, ctx, role: discord.Role):

        await self.bot.config.set("priority_staff_role", role.id)

        await ctx.send(
            f"Priority staff role set to {role.mention}"
        )


    # SET STAFF MESSAGE
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
    await bot.add_cog(PrioSupport(bot))