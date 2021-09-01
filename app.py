import os
import discord
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

from config.main import (
    token,
    bot_prefix,
    owner_id,
    color
)

menu = DefaultMenu(page_left="⬅", page_right="➡",
                   remove="⛔", active_time=120)

# Custom ending note
ending_note = "The power of {ctx.bot.user.name} 🔱"

# Intents
intents = discord.Intents.all()
# The bot
bot = commands.Bot(command_prefix=bot_prefix, intents=intents,
                   owner_id=owner_id, help_command=PrettyHelp(menu=menu, color=color, ending_note=ending_note))

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print(f" Discord version = {discord.__version__}")

    await bot.change_presence(
        activity=discord.Game(
            name=f"{bot.command_prefix}help - By DroidZed"
        )
    )
bot.run(token)
