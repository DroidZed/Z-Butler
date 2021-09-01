from discord import Member
from discord.ext.commands import Cog, Context, Bot, command

from config.embed import create_embed, pfp_config


class UserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="pfp",
        usage="<username>",
        description="Ban a user for a specific reason.")
    async def pfp(self, ctx: Context, member: Member = None):

        if not member:
            member = ctx.message.author

        await ctx.send(
            embed=create_embed(
                config=pfp_config(
                    url=member.avatar_url,
                    tag=f'{member.name}#{member.discriminator}',
                    issuer=f'{ctx.message.author}',
                    avatar_url=member.avatar_url
                )
            )
        )


def setup(bot: Bot):
    bot.add_cog(UserCog(Cog))
