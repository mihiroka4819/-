import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"ログイン: {bot.user}")

@bot.tree.command(name="chara", description="キャラシを作る")
@app_commands.describe(
    name="名前",
    race="種族",
    age="年齢",
    desc="説明",
    image="画像URL（任意）"
)
async def chara(
    interaction: discord.Interaction,
    name: str,
    race: str,
    age: int,
    desc: str,
    image: str = None
):

    embed = discord.Embed(
        title="📄 キャラクターシート",
        color=discord.Color.purple()
    )

    embed.add_field(name="名前", value=name, inline=False)
    embed.add_field(name="種族", value=race, inline=False)
    embed.add_field(name="年齢", value=str(age), inline=False)
    embed.add_field(name="説明", value=desc, inline=False)

    if image:
        embed.set_image(url=image)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="roulette", description="選択肢からランダムで1つ選ぶ")
@app_commands.describe(
    choices="カンマ区切りで選択肢を入力してください"
)
async def roulette(interaction: discord.Interaction, , choices: str):  # ← を付けた
    options = [choice.strip() for choice in choices.split(",") if choice.strip()]
    if not options:
        await interaction.response.send_message("選択肢がありません！", ephemeral=True)
        return

    selected = random.choice(options)
    await interaction.response.send_message(f"🎲 ルーレット結果: {selected}")

import os
bot.run(os.environ["TOKEN"])
