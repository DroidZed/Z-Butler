import os

from discord import Intents, Game
from discord.ext import commands

from classes.help import ZedHelpCommand
from classes.mongo_db_management import MongoDBConnection
from config.main import OWNER_ID, PREFIX, TOKEN
from functions.helpers import print_msg

# Intents
intents = Intents.all()

# The bot
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(PREFIX), # type: ignore
    intents=intents,
    owner_id=OWNER_ID,
    help_command=ZedHelpCommand(),
)

# Load cogs
if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print_msg()

    await bot.change_presence(
        activity=Game(name=f"{PREFIX}help - By DroidZed")
    )

    MongoDBConnection()


bot.run(TOKEN)
