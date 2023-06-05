from typing import Mapping, Optional, List

from discord.ext.commands import HelpCommand, Cog, Command

from config import Env

from modules.embedder import (
    ZembedField,
    generate_embed,
)


class ZedHelpCommand(HelpCommand):
    """Help command for those seeking the power of Z"""

    def __init__(self):
        super().__init__()
        self._default_footer_text = (
            "The power of The Z Butler 🔱"
        )
        self._default_footer_img = "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"

    async def send_bot_help(
        self, mapping: Mapping[Optional[Cog], List[Command]]
    ):
        commands = tuple(
            ZembedField(
                rep.qualified_name,
                " ".join(
                    f"`{cmd}`" for cmd in rep.get_commands()
                ),
                False,
            )
            for rep in mapping
            if rep
            and rep.qualified_name != "Event Handlers"
        )

        embed = generate_embed(
            title="Help Command",
            color=Env.BOT_COLOR,
            description="Showing you the list of my powers, write Zhelp <command name> | <category name> for more info on those.",
            footer_text=self._default_footer_text,
            footer_icon=self._default_footer_img,
            *commands,
        )

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: Cog):
        if cog.qualified_name in {"Event Handlers"}:
            return

        commands = tuple(
            ZembedField(
                cmd.name,
                cmd.description,
                False,
            )
            for cmd in cog.walk_commands()
        )

        embed = generate_embed(
            title=cog.qualified_name,
            color=Env.BOT_COLOR,
            description=cog.description,
            footer_text=self._default_footer_text,
            footer_icon=self._default_footer_img,
            *commands,
        )

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: Command):
        desc = [
            ZembedField(
                "Aliases",
                " | ".join(
                    f"`{a}`" for a in command.aliases if a
                ),
                False,
            ),
            ZembedField("Usage", f"{command.usage}", False),
        ]

        embed = generate_embed(
            title=command.name,
            color=Env.BOT_COLOR,
            description=command.description,
            footer_text=self._default_footer_text,
            footer_icon=self._default_footer_img,
            *desc,
        )

        await self.get_destination().send(embed=embed)
