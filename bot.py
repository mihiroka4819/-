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
async def roulette(interaction: discord.Interaction, *, choices: str):
    # 空白除去、全角カンマを半角に変換
    choices = choices.replace("，", ",")
    options = [c.strip() for c in choices.split(",") if c.strip()]
    
    if not options:
        await interaction.response.send_message("選択肢がありません！", ephemeral=True)
        return

    selected = random.choice(options)

    # 埋め込み作成
    embed = discord.Embed(
        title="🎲 ルーレット結果",
        color=discord.Color.green()
    )
    # 選択肢一覧は最大500文字まで切り詰め
    embed.add_field(name="選択肢一覧", value=", ".join(options)[:500], inline=False)
    embed.add_field(name="選ばれたもの", value=f"**{selected}**", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="roll", description="クトゥルフ風ダイスロール（1d100推奨）")
@app_commands.describe(
    dice="例: 1d100 / 3d6 など", 
    target="成功判定の目標値（省略可、1d100で使う）"
)
async def roll(interaction: discord.Interaction, *, dice: str, target: int = None):
    dice = dice.replace(" ", "")  # 空白削除
    try:
        count_str, sides_str = dice.lower().split("d")
        count = int(count_str)
        sides = int(sides_str)
    except:
        await interaction.response.send_message(
            "形式は XdY で入力してください（例: 1d100, 3d6）", ephemeral=True
        )
        return

    if count <= 0 or sides <= 0:
        await interaction.response.send_message(
            "正の整数を入力してください", ephemeral=True
        )
        return

    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)

    embed = discord.Embed(
        title="🎲 ダイスロール結果",
        color=discord.Color.dark_purple()
    )
    embed.add_field(name="振ったダイス", value=f"{dice}", inline=False)
    embed.add_field(name="出目", value=", ".join(map(str, rolls)), inline=False)
    embed.add_field(name="合計", value=str(total), inline=False)

    # 1d100用に成功判定
    if sides == 100 and count == 1 and target is not None:
        roll_value = rolls[0]
        if roll_value == 1:
            result_text = "大成功"
        elif roll_value <= target // 5:
            result_text = "大成功"
        elif roll_value <= target // 2:
            result_text = "成功（1/2成功）"
        elif roll_value <= target:
            result_text = "成功"
        elif roll_value >= 96:
            result_text = "💀 大失敗"
        else:
            result_text = "失敗"
        embed.add_field(name=f"目標値: {target}", value=result_text, inline=False)

    await interaction.response.send_message(embed=embed)

import os
bot.run(os.environ["TOKEN"])
