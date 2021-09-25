import os
from platform import python_version

from discord import Intents, Game, __version__
from discord.ext import commands

from classes.help import ZedHelpCommand
from classes.print_codes import (GREEN, NOCOLOR, ITALIC, NORMAL, CYAN, BLUE)
from config.main import PREFIX, OWNER_ID, TOKEN

# Intents
intents = Intents.all()
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
    print("/" * 39)
    print(" ----------\\")
    print(f" |       {CYAN}*{NOCOLOR}  |         /\\")
    print(" --------   |        /  \\")
    print("       /   /         \\   \\")
    print("      /   /          /   /")
    print(f"     /   / {BLUE}The Z Bot{NOCOLOR} \\   \\")
    print("    |   -------------/   /")
    print(f"    |       {GREEN}ONLINE{NOCOLOR}      /")
    print("     ------------------")
    print(f"| Discord version: {__version__}               |", end="\n")
    print(f"| Running under: {ITALIC}Python v{python_version()}{NORMAL}         |", end="\n")
    print("/" * 39)

    await bot.change_presence(
        activity=Game(
            name=f"{bot.command_prefix}help - By DroidZed"
        )
    )


bot.run(TOKEN)
