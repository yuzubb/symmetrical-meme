import discord
from discord import app_commands
from discord.ext import commands
import sys
import os
from utils import OWNER_ID


def is_owner_check():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("このコマンドはオーナーのみ使用できます", ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)


class RestartCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="再起動", description="Botを再起動します（オーナー専用）")
    @is_owner_check()
    async def restart(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔄 再起動中...",
            description="Botを再起動します。数秒後に復帰します。",
            color=0xF39C12
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.bot.close()
        os.execv(sys.executable, [sys.executable] + sys.argv)


async def setup(bot: commands.Bot):
    await bot.add_cog(RestartCog(bot))
