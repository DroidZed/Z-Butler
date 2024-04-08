import asyncio
import os

from discord import Intents, Game
from discord.ext import commands

from utils import print_msg, Env
from modules import ZedHelpCommand, MongoDBConnection

# Intents
intents = Intents.all()

# The bot
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(Env.PREFIX),  # type: ignore
    intents=intents,
    owner_id=Env.OWNER_ID,
    help_command=ZedHelpCommand(),
)

# Load cogs
if __name__ == "__main__":
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print_msg()

    await bot.change_presence(
        activity=Game(name=f"{Env.PREFIX}help - By DroidZed")
    )

    MongoDBConnection()


bot.run(Env.TOKEN)
