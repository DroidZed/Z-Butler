import os
from platform import python_version

import rich as rch
from discord import Game, Intents, version_info
from discord.ext.commands import Bot

from modules import ZedHelpCommand
from modules.logging import LoggerHelper
from utils import Env


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
        self.__print_msg()

        await self.change_presence(
            activity=Game(name=f"{Env.PREFIX}help - By DroidZed")
        )

        LoggerHelper().info("Bot started")

    def __print_msg(self) -> None:
        rch.print("/" * 39)
        rch.print(" ----------\\")
        rch.print(" |       [b cyan]*[/]  |         [white]/[/]\\")
        rch.print(" --------   |        /  \\")
        rch.print("       /   /         \\   \\")
        rch.print("      /   /          /   /")
        rch.print("     [white]/[/]   [white]/[/] [b blue]The Z Bot[/] \\   \\")
        rch.print("    |   --------------   /")
        rch.print("    |       [b green]ONLINE[/]      [white]/[/]")
        rch.print("     ------------------")
        rch.print(
            f"[b white]|[b]         [i]By: [purple]DroidZed[/purple][/i]{' ' * 16}|"
        )
        rch.print(
            f"[b white]|[b] Discord version: [u blue]{version_info.major}.{version_info.minor}.{version_info.micro if version_info.micro else 0}[/u blue]{' ' * 14}|",
            end="\n",
        )
        rch.print(
            f"[b white]| Running under: [i yellow]Python v{python_version()}[/i yellow] :snake:    |",
            end="\n",
        )  # Don't remove the extra space added after the snake emoji, it was added so the bars will align in the console
        # of the hosting.
        rch.print("/" * 39)
