import os
from discord import Game, Intents
from discord.ext.commands import Bot

from modules.logging import LoggerHelper
from modules.mongo import MongoDBConnection
from modules import ZedHelpCommand
from utils import Env, print_msg


class ZBot(Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=Env.PREFIX,
            intents=Intents.all(),
            owner_id=Env.OWNER_ID,
            help_command=ZedHelpCommand(),
        )

        # Load cogs
        for filename in os.listdir("./src/cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self) -> None:
        print_msg()

        await self.change_presence(
            activity=Game(name=f"{Env.PREFIX}help - By DroidZed")
        )

        MongoDBConnection()

        LoggerHelper().info("Bot started")
