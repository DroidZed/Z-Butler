from discord.abc import Messageable
from discord.ext.commands import HelpCommand, Cog, Command

from config.embed.help import help_config
from functions.embed_factory import create_embed


class ZedHelpCommand(HelpCommand):
    """Help command for those seeking the power of Z"""

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        dest: Messageable = self.get_destination()

        dic = {
            cog.qualified_name: ' '.join(
                f'`{command.name}`' for command in mapping[cog]
            )
            for cog in mapping
            if cog
        }

        del dic["Event Handlers"]

        embed = create_embed(config=help_config(),
                             reason=None,
                             cfg_type=None, **dic)

        await dest.send(embed=embed)

    async def send_cog_help(self, cog: Cog):
        if cog.qualified_name == "Event Handlers":
            return

        dest: Messageable = self.get_destination()

        cmds = cog.get_commands()

        names = [n.name for n in cmds]

        desc = [f'`{n.description}`' for n in cmds]

        dic = dict(zip(names, desc))

        embed = create_embed(config=help_config(cog.qualified_name, cog.description),
                             reason=None,
                             cfg_type=None, **dic)

        await dest.send(embed=embed)

    async def send_command_help(self, command: Command):
        dest: Messageable = self.get_destination()

        dic = {
            "Aliases": " | ".join(f'`{a}`' for a in command.aliases if a),
            "Usage": command.usage,
        }

        embed = create_embed(config=help_config(command.name, command.description),
                             reason=None,
                             cfg_type=None, **dic)

        await dest.send(embed=embed)
