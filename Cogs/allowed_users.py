import discord
from discord import app_commands
from discord.ext import commands
from utils import OWNER_ID, load_allowed_users, save_allowed_users


def is_owner_check():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("このコマンドはオーナーのみ使用できます", ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)


class AllowedUsersCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="許可ユーザー追加", description="コマンドを使用できるユーザーを追加します（オーナー専用）")
    @app_commands.describe(user="追加するユーザー")
    @is_owner_check()
    async def add_allowed_user(self, interaction: discord.Interaction, user: discord.User):
        allowed = load_allowed_users()

        if user.id in allowed:
            return await interaction.response.send_message(
                f"{user.mention} はすでに許可リストに登録されています",
                ephemeral=True
            )

        allowed.append(user.id)
        save_allowed_users(allowed)

        embed = discord.Embed(
            title="✅ 許可ユーザー追加",
            description=f"{user.mention} をコマンド許可リストに追加しました",
            color=0x2ECC71
        )
        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
        embed.add_field(name="現在の許可ユーザー数", value=f"{len(allowed)}人")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="許可ユーザー削除", description="コマンドの使用許可を削除します（オーナー専用）")
    @app_commands.describe(user="削除するユーザー")
    @is_owner_check()
    async def remove_allowed_user(self, interaction: discord.Interaction, user: discord.User):
        allowed = load_allowed_users()

        if user.id not in allowed:
            return await interaction.response.send_message(
                f"{user.mention} は許可リストに登録されていません",
                ephemeral=True
            )

        allowed.remove(user.id)
        save_allowed_users(allowed)

        embed = discord.Embed(
            title="🗑️ 許可ユーザー削除",
            description=f"{user.mention} をコマンド許可リストから削除しました",
            color=0xE74C3C
        )
        embed.add_field(name="現在の許可ユーザー数", value=f"{len(allowed)}人")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="許可ユーザー一覧", description="コマンドを使用できるユーザーの一覧を表示します（オーナー専用）")
    @is_owner_check()
    async def list_allowed_users(self, interaction: discord.Interaction):
        allowed = load_allowed_users()

        if not allowed:
            return await interaction.response.send_message(
                "許可ユーザーは登録されていません\n（オーナーは常に使用可能です）",
                ephemeral=True
            )

        lines = [f"<@{uid}>" for uid in allowed]
        embed = discord.Embed(
            title="📋 許可ユーザー一覧",
            description="\n".join(lines),
            color=0x3498DB
        )
        embed.set_footer(text=f"合計 {len(allowed)}人 ／ オーナーは常に使用可能")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(AllowedUsersCog(bot))
