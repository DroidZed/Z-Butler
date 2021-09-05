from config.embed.pfp import pfp_config
from discord import Member
from discord.ext.commands import Bot, BucketType, Cog, Context, command
from discord.ext.commands.core import cooldown
from functions.embed_factory import create_embed
from config.main import PREFIX


class UserCog(Cog, name="User-related Commands", description="User commands for everyone"):

    def __init__(self, bot: Bot):
        self.bot = bot
        self._last_member = None

    @command(
        name="pic",
        usage=f"{PREFIX}pic `username`",
        description="Display the requested user's profile picture.",
        aliases=['pfp'])
    @cooldown(1, 5, BucketType.user)
    async def pfp(self, ctx: Context, member: Member = None):
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
    async def hello(self, ctx: Context, *, member: Member = None):
        member = member or ctx.author
        await ctx.message.delete()
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello <@{member.id}>~')
        else:
            await ctx.send(f'Hello <@{member.id}>... This feels familiar.')
        self._last_member = member


def setup(bot: Bot):
    bot.add_cog(UserCog(Cog))
