from discord import (Embed, Member)
from discord.ext.commands import (
    cooldown,
    Bot,
    Cog,
    command,
    Context
)


class StatsCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def server_info(self, ctx: Context):

        await ctx.send("Server info !")


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
