from config.embed.hello import hello_config
from config.embed.pfp import pfp_config
from config.main import PREFIX
from discord.ext.commands import (Bot, BucketType, Cog, Context,
                                  MemberConverter, command)
from discord.ext.commands.core import cooldown
from functions.embed_factory import create_embed
from functions.find_gif import find_gif


class UserCog(Cog, name="User-related Commands", description="User commands for everyone"):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="pic",
        usage=f"{PREFIX}pic `username`",
        description="Display the requested user's profile picture.",
        aliases=['pfp'])
    @cooldown(1, 5, BucketType.user)
    async def pfp(self, ctx: Context, member: MemberConverter = None):
        if not member:
            member = ctx.message.author

        await ctx.send(
            embed=create_embed(
                config=pfp_config(
                    url=member.avatar_url,
                    tag=f'{member.name}#{member.discriminator}',
                    issuer=f'{ctx.message.author}',
                    avatar_url=f'{ctx.message.author.avatar_url}'
                )
            )
        )

    @command(
        name="greet",
        usage=f"{PREFIX}greet `username`",
        description="Greet a given user",
        aliases=['grt'])
    @cooldown(1, 3, BucketType.user)
    async def hello(self, ctx: Context, *, member: MemberConverter = None):
        member = member or ctx.author

        if result_set := await find_gif("Hello"):
            await ctx.message.delete()
            await ctx.send(
                embed=create_embed(
                    hello_config(
                        message=f'Hello <@{member.id}>~ 👋🏻',
                        url=result_set['media'][0]['gif']['url'])
                )
            )


def setup(bot: Bot):
    bot.add_cog(UserCog(bot))
