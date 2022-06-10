from discord import Spotify, Game, Streaming, Activity, CustomActivity
from discord.ext.commands import (
    Bot,
    BucketType,
    Cog,
    Context,
    MemberConverter,
    command,
    cooldown,
)
from discord.ext.tasks import loop

from api.images import find_gif
from api.twitch import get_pfp
from classes.embed_factory import EmbedFactory
from classes.twitch_client import TwitchClient, authenticate
from config.colors import BOT_COLOR
from config.embed.activity import activity_config, streaming_activity_config, playing_activity_config, spotify_config
from config.main import PREFIX, CROWN_ROLE_ID


class UserCog(Cog, name="User-Commands", description="👤 User commands for everyone"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.decrement_token_validity.start()

    def cog_unload(self):
        self.decrement_token_validity.stop()

    @command(
        name="pic",
        usage=f"{PREFIX}pic `username`",
        description="Display the requested user's profile picture.",
        aliases=["pfp"],
    )
    @cooldown(1, 5, BucketType.user)
    async def pfp(self, ctx: Context, member: MemberConverter = None):

        member = member or ctx.author

        await ctx.send(
            embed=EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    title=f"**{'Lord  👑 **𝕯𝖗𝖔𝖎𝖉𝖅𝖊𝖉** 👑' if member.id == CROWN_ROLE_ID else f'{member.name}#{member.discriminator}'}**'s Profile Picture",
                    color=BOT_COLOR,
                    image={"url": member.avatar_url},
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={
                        "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
                    },
                    footer={
                        "text": f"Requested by {ctx.message.author} 💙",
                        "icon_url": f"{ctx.message.author.avatar_url}",
                    },
                )
            )
        )

    @command(
        name="greet",
        usage=f"{PREFIX}greet `username`",
        description="Greet a given user",
        aliases=["grt"],
    )
    @cooldown(1, 3, BucketType.user)
    async def hello(self, ctx: Context, *, member: MemberConverter = None):

        member = member or ctx.author

        async with ctx.typing():
            result_set = await find_gif("Hello")

        await ctx.message.delete()
        await ctx.send(
            embed=EmbedFactory.create_embed(
                EmbedFactory.create_config(
                    title="Z Butler's Greeting",
                    color=BOT_COLOR,
                    description=f"Hello <@{member.id}>~ 👋🏻",
                    image={"url": f"{result_set['media'][0]['gif']['url']}"},
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={
                        "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
                    },
                )
            )
        )

    @command(
        name="status",
        description="Get the status of a user, can be either a `song`, a `game`, a `stream` or any `custom "
        "activity`.\n Ignoring the bio.",
        usage=f"{PREFIX}status `username`",
        aliases=["st?"],
    )
    @cooldown(1, 7, BucketType.user)
    async def status(self, ctx: Context, member: MemberConverter = None) -> None:

        member = member or ctx.author

        if not member.activities:
            if member == ctx.author:
                await ctx.message.reply(
                    "https://pics.me.me/thumb_c-mon-do-something-me-irl-38375559.png",
                    mention_author=True,
                )
            else:
                await ctx.send(f"{member.mention}")
                await ctx.send("https://pics.me.me/thumb_c-mon-do-something-me-irl-38375559.png")
            return

        acts = member.activities

        if all(isinstance(e, CustomActivity) for e in acts):

            if member == ctx.author:
                await ctx.message.reply(
                    "Try again later with someone who's actually doing something, "
                    "not a snob like you wasting his life energy instead of being a "
                    "useful human being... 🙄",
                    mention_author=True,
                )
            else:
                await ctx.send(f"{member.mention} Go listen to some music or do something in your life 🙄")
            return

        act = (acts[1:])[0] if len(acts) > 1 else acts[0]

        config: dict = {}

        match act:
            case Spotify():
                async with ctx.typing():
                    config = spotify_config(
                        mention=member.mention,
                        song=act.title,
                        album=act.album,
                        artist=act.artist,
                        art=act.album_cover_url,
                        link=f"https://open.spotify.com/track/{act.track_id}",
                    )

            case Game():
                async with ctx.typing():
                    config = playing_activity_config(
                        name=act.name,
                        mention=member.mention,
                        issuer=ctx.author,
                        avatar_url=ctx.message.author.avatar_url,
                        since=act.start.strftime("%x %X") if act.start else None,
                    )

            case Streaming():
                async with ctx.typing():
                    streamer_image_url: str | None = await get_pfp(act.url[22:])

                    if not streamer_image_url.startswith("https://"):
                        streamer_image_url = None

                    config = streaming_activity_config(
                        name=act.name,
                        mention=member.mention,
                        issuer=ctx.author,
                        avatar_url=ctx.message.author.avatar_url,
                        platform=act.platform,
                        stream_url=act.url,
                        streamed_game=act.game,
                        streamer_pfp=streamer_image_url,
                    )

            case Activity():
                async with ctx.typing():
                    config = activity_config(
                        name=act.name,
                        username=member.name,
                        issuer=ctx.author,
                        avatar_url=ctx.message.author.avatar_url,
                        image_url=act.large_image_url,
                        since=act.start.strftime("%x %X") if act.start else None,
                    )

        if not config:
            await ctx.send("Nothing, move along....")
            return

        await ctx.send(embed=EmbedFactory.create_embed(config))
        return

    @loop(hours=24, reconnect=True)
    async def decrement_token_validity(self):

        TwitchClient().decrement_expiration()

    @decrement_token_validity.before_loop
    async def before_token_decrement(self):

        TwitchClient(await authenticate())

        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(UserCog(bot))
