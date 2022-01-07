import os
from platform import python_version

import rich as rch
from discord import Intents, Game, __version__
from discord.ext import commands

from classes.help import ZedHelpCommand
from classes.mongo_db_connection import MongoDBConnection
from config.main import PREFIX, OWNER_ID, TOKEN

# Intents
intents = Intents.all()
# The bot
bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    owner_id=OWNER_ID,
    help_command=ZedHelpCommand(),
)

# Load cogs
if __name__ == "__main__":
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print("Hello World !!")

    print("/" * 39)
    print(" ----------\\")
    rch.print(f" |       [b cyan]*[/]  |         [white]/[/]\\")
    print(" --------   |        /  \\")
    print("       /   /         \\   \\")
    print("      /   /          /   /")
    rch.print(f"     [white]/[/]   [white]/[/] [b blue]The Z Bot[/] \\   \\")
    print("    |   --------------   /")
    rch.print(f"    |       [b green]ONLINE[/]      [white]/[/]")
    print("     ------------------")
    rch.print(f"|[b]         [i]By: [purple]DroidZed[/purple]{' ' * 17}|")
    rch.print(f"|[b] Discord version: [u blue]{__version__}[/u blue]               |", end="\n")
    rch.print(
        f"[b white]| Running under: Python v{python_version()}        |",
        end="\n",
    )
    print("/" * 39)

    await bot.change_presence(activity=Game(name=f"{bot.command_prefix}help - By DroidZed"))

    MongoDBConnection()


bot.run(TOKEN)
