from discord import Member
from discord.ext.commands import (
    Bot,
    Cog,
    command,
    Context
)


class GreetingsCog(Cog, name="greeting command"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._last_member = None

    @command(
        name="greet",
        usage="<username>",
        description="Greets the user",
        aliases=['grt']
    )
    async def hello(self, ctx: Context, *, member: Member = None):
        """Says hello"""
        member = member or ctx.author
        await ctx.message.delete()
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello <@{member.id}>~')
        else:
            await ctx.send(f'Hello <@{member.id}>... This feels familiar.')
        self._last_member = member


def setup(bot: Bot):
    bot.add_cog(GreetingsCog(bot))
