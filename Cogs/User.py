from discord import (Spotify, Game, Streaming, Activity, CustomActivity)
from discord.ext.commands import (Bot,
                                  BucketType,
                                  Cog,
                                  Context,
                                  MemberConverter,
                                  command,
                                  cooldown)

from config.embed.activity import activity_config
from config.embed.hello import hello_config
from config.embed.pfp import pfp_config
from config.embed.playing_act import playing_activity_config
from config.embed.spotify import spotify_config
from config.embed.streaming_act import streaming_activity_config
from config.main import PREFIX
from functions.embed_factory import create_embed
from functions.find_gif import find_gif


class UserCog(Cog, name="User-Commands", description="👤 User commands for everyone"):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="pic",
        usage=f"{PREFIX}pic `username`",
        description="Display the requested user's profile picture.",
        aliases=["pfp"])
    @cooldown(1, 5, BucketType.user)
    async def pfp(self, ctx: Context, member: MemberConverter = None):
        if not member:
            member = ctx.message.author

        async with ctx.typing():
            embed = create_embed(
                config=pfp_config(
                    url=str(member.avatar_url),
                    tag=f'{member.name}#{member.discriminator}',
                    issuer=f'{ctx.message.author}',
                    avatar_url=f'{ctx.message.author.avatar_url}'
                )
            )

        await ctx.send(embed=embed)

    @command(
        name="greet",
        usage=f"{PREFIX}greet `username`",
        description="Greet a given user",
        aliases=["grt"])
    @cooldown(1, 3, BucketType.user)
    async def hello(self, ctx: Context, *, member: MemberConverter = None):
        member = member or ctx.author

        async with ctx.typing():
            result_set = await find_gif("Hello")

        if result_set:
            await ctx.message.delete()
            await ctx.send(
                embed=create_embed(
                    hello_config(
                        message=f'Hello <@{member.id}>~ 👋🏻',
                        url=result_set['media'][0]['gif']['url'])
                )
            )

    @command(
        name="status",
        description="Get the status of a user, can be either a `song`, a `game`, a `stream` or any `custom "
                    "activity`.\n Ignoring the bio.",
        usage=f"{PREFIX}status `username`",
        aliases=["st?"]
    )
    async def status(self, ctx: Context, member: MemberConverter = None) -> None:

        member = member or ctx.author

        if not member.activities:
            await ctx.message.reply("https://pics.me.me/thumb_c-mon-do-something-me-irl-38375559.png")
            return

        acts = member.activities

        if all(isinstance(e, CustomActivity) for e in acts):
            await ctx.message.reply("Go listen to some music or do something in your life then try again later 🙄")
            return

        act = (acts[1:])[0] if len(acts) > 1 else acts[0]

        config: dict = {}

        if isinstance(act, Spotify):
            config = spotify_config(
                member.mention,
                act.title,
                act.album,
                act.artist,
                act.album_cover_url,
                f"https://open.spotify.com/track/{act.track_id}")

        if isinstance(act, Game):
            config = playing_activity_config(
                act.name,
                member.mention,
                ctx.author,
                ctx.message.author.avatar_url,
                act.start.strftime('%x %X') if act.start else None
            )

        if isinstance(act, Streaming):
            config = streaming_activity_config(
                act.name,
                member.mention,
                ctx.author,
                ctx.message.author.avatar_url,
                act.platform,
                act.url,
                act.game
            )

        if isinstance(act, Activity):
            config = activity_config(
                act.name,
                member.name,
                ctx.author,
                ctx.message.author.avatar_url,
                act.large_image_url,
                act.start.strftime('%x %X') if act.start else None
            )

        if not config:
            await ctx.send("Nothing, move along....")
            return

        await ctx.send(embed=create_embed(config))
        return


def setup(bot: Bot):
    bot.add_cog(UserCog(bot))
