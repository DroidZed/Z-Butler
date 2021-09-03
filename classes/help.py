from discord.abc import Messageable
from config.embed import help_config
from discord.ext.commands import HelpCommand
from functions.embed_factory import create_embed


class ZedHelpCommand(HelpCommand):

    """Help command for those seeking the power of Z"""

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        dest: Messageable = self.get_destination()

        dic = {cog.qualified_name: ' '.join(
            [f'`{command.name}`' for command in mapping[cog]]
        )
            for cog in mapping if cog}.pop('Event Handlers')

        config = help_config()
        embed = create_embed(config=config, reason=None,
                             no_perms_type=None, **dic)

        await dest.send(embed=embed)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)

    async def send_command_help(self, command):
        return await super().send_command_help(command)
