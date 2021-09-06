import os

import discord
from discord.ext import commands

from classes.help import ZedHelpCommand
from config.main import PREFIX, OWNER_ID, TOKEN

# Intents
intents = discord.Intents.all()
# The bot
bot = commands.Bot(command_prefix=PREFIX,
                   intents=intents, owner_id=OWNER_ID,
                   help_command=ZedHelpCommand())

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
bot.run(TOKEN)
