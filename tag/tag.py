from discord.ext import commands
import discord

from core.models import PermissionLevel
from core import checks


class TicketTags(commands.Cog):
    """Adds tag support to Modmail tickets."""

    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.api.get_plugin_partition(self)

    async def get_tags(self, channel_id):
        data = await self.coll.find_one({"channel_id": channel_id})
        if not data:
            return []
        return data.get("tags", [])

    async def save_tags(self, channel_id, tags):
        await self.coll.update_one(
            {"channel_id": channel_id},
            {"$set": {"tags": tags}},
            upsert=True
        )

    async def update_topic(self, thread, tags):
        base = thread.channel.topic or ""
        tag_text = f" | tags: {', '.join(tags)}" if tags else ""

        if "| tags:" in base:
            base = base.split("| tags:")[0].strip()

        new_topic = base + tag_text

        try:
            await thread.channel.edit(topic=new_topic)
        except:
            pass

    @commands.group(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def tag(self, ctx):
        """Manage ticket tags."""
        await ctx.send("Usage: tag add/remove/list")

    @tag.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def add(self, ctx, *, tag: str):

        thread = ctx.thread
        tags = await self.get_tags(thread.channel.id)

        tag = tag.lower()

        if tag in tags:
            return await ctx.send("Tag already exists.")

        if len(tags) >= 5:
            return await ctx.send("Maximum of 5 tags per ticket.")

        tags.append(tag)
        await self.save_tags(thread.channel.id, tags)
        await self.update_topic(thread, tags)

        await ctx.send(f"🏷 Tag `{tag}` added.")

    @tag.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def remove(self, ctx, *, tag: str):

        thread = ctx.thread
        tags = await self.get_tags(thread.channel.id)

        tag = tag.lower()

        if tag not in tags:
            return await ctx.send("Tag not found.")

        tags.remove(tag)

        await self.save_tags(thread.channel.id, tags)
        await self.update_topic(thread, tags)

        await ctx.send(f"🗑 Tag `{tag}` removed.")

    @tag.command()
    async def list(self, ctx):

        thread = ctx.thread
        tags = await self.get_tags(thread.channel.id)

        if not tags:
            return await ctx.send("This ticket has no tags.")

        embed = discord.Embed(
            title="🏷 Ticket Tags",
            description=", ".join(f"`{t}`" for t in tags),
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(TicketTags(bot))