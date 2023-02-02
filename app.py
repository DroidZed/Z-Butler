import os
from platform import python_version

import rich as rch
from discord import Intents, Game
from discord import version_info
from discord.ext import commands

from classes.help import ZedHelpCommand
from classes.mongo_db_management import MongoDBConnection
from classes.twitter_ import TweepyWrapper
from config.main import OWNER_ID, PREFIX, TOKEN

# Intents
intents = Intents.all()

# The bot
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(PREFIX),
    intents=intents,
    owner_id=OWNER_ID,
    help_command=ZedHelpCommand()
)

# Load cogs
if __name__ == "__main__":
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print("/" * 39)
    print(" ----------\\")
    rch.print(" |       [b cyan]*[/]  |         [white]/[/]\\")
    print(" --------   |        /  \\")
    print("       /   /         \\   \\")
    print("      /   /          /   /")
    rch.print("     [white]/[/]   [white]/[/] [b blue]The Z Bot[/] \\   \\")
    print("    |   --------------   /")
    rch.print("    |       [b green]ONLINE[/]      [white]/[/]")
    print("     ------------------")
    rch.print(f"|[b]         [i]By: [purple]DroidZed[/purple][/i]{' ' * 17}|")
    rch.print(f"|[b] Discord version: [u blue]{version_info.build}[/u blue]{' ' * 15}|", end="\n")
    rch.print(
        f"[b white]| Running under: [i yellow]Python v{python_version()}[/i yellow] :snake:      |",
        end="\n",
    )  # Don't remove the extra space added after the snake emoji, it was added so the bars will align in the console
    # of the hosting.
    print("/" * 39)

    await bot.change_presence(activity=Game(name=f"{bot.command_prefix}help - By DroidZed"))

    MongoDBConnection()

    TweepyWrapper()


bot.run(TOKEN)
