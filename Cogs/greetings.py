from discord import Member
from discord.ext import commands


class GreetingsCog(commands.Cog, name="greeting command"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(
        name="hello",
        usage="<username>",
        description="Greets the user")
    async def hello(self, ctx, *, member: Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello <@{member.id}>~')
        else:
            await ctx.send(f'Hello <@{member.id}>... This feels familiar.')
        self._last_member = member


def setup(bot: commands.Bot):
    bot.add_cog(GreetingsCog(bot))
