from discord import Member
from discord.ext.commands import Cog, Context, Bot, command

from config.embed import createEmbed, pfp_config


class UserCog(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(
        name="pfp",
        usage="<username>",
        description="Ban a user for a specific reason.")
    async def pfp(self, ctx: Context, member: Member = None):

        if not member:
            member = ctx.message.author
        await ctx.send(embed=createEmbed(config=pfp_config(member.avatar_url, f'{member.name}#{member.discriminator}')))


def setup(bot):
    bot.add_cog(UserCog(Cog))
