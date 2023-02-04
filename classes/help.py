from discord.ext.commands import HelpCommand, Cog, Command

from classes.embed_factory import EmbedFactory
from config.colors import BOT_COLOR


class ZedHelpCommand(HelpCommand):
    """Help command for those seeking the power of Z"""

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        dic = {cog.qualified_name: " ".join(f"`{command.name}`" for command in mapping[cog]) for cog in mapping if cog}

        del dic["Event Handlers"]

        await self.get_destination().send(
            embed=EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    title="Help Command",
                    color=BOT_COLOR,
                    description="Showing you the list of my powers, write Zhelp <command name> | <category name> for more info on those.",
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    footer={
                        "text": "The power of The Z Butler 🔱",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                ),
                **dic,
            )
        )

    async def send_cog_help(self, cog: Cog):
        if cog.qualified_name in {"Event Handlers"}:
            return

        cmds = cog.get_commands()

        await self.get_destination().send(
            embed=EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    title=cog.qualified_name,
                    color=BOT_COLOR,
                    description=cog.description,
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    footer={
                        "text": "The power of The Z Butler 🔱",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                ),
                **dict(zip([n.name for n in cmds], [f"`{n.description}`" for n in cmds])),
            )
        )

    async def send_command_help(self, command: Command):
        await self.get_destination().send(
            embed=EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    title=command.name,
                    color=BOT_COLOR,
                    description=command.description,
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    footer={
                        "text": "The power of The Z Butler 🔱",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                ),
                **{
                    "Aliases": " | ".join(f"`{a}`" for a in command.aliases if a),
                    "Usage": command.usage,
                },
            )
        )
