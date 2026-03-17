import discord
from discord.ext import commands

from core.models import getLogger

logger = getLogger(__name__)


class CloseButtonView(discord.ui.View):
    def __init__(self, bot, user):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        # Only ticket owner can press
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("You can't close this ticket.", ephemeral=True)
            return

        thread = await self.bot.threads.find(self.user.id)
        if thread is None or thread.closed:
            await interaction.response.send_message("Thread already closed.", ephemeral=True)
            return

        await interaction.response.defer()

        try:
            await thread.close(
                closer=interaction.user,
                message="User closed the ticket using the button.",
                silent=False
            )
        except Exception as e:
            logger.error(f"[CloseButton] Failed: {e}")


class CloseButton(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_reply(self, thread, from_mod, message, anonymous, plain):

        if not from_mod:
            return

        try:
            view = CloseButtonView(self.bot, thread.recipient)
            await message.edit(view=view)
        except Exception as e:
            logger.warning(f"[CloseButton] Failed to attach button: {e}")


async def setup(bot):
    await bot.add_cog(CloseButton(bot))