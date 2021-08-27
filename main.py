import os
import discord
from decouple import config
from discord.ext import commands
from discord.partial_emoji import PartialEmoji

# Get configuration from env.

token = config('API_TOKEN')
prefix = config('PREFIX')
owner_id = config('OWNER_ID')

# Intents
intents = discord.Intents.all()
# The bot
bot = commands.Bot(prefix, intents=intents, owner_id=owner_id)

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
