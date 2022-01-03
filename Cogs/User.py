from discord import (Spotify, Game, Streaming, Activity, CustomActivity)
from discord.ext.commands import (Bot,
                                  BucketType,
                                  Cog,
                                  Context,
                                  MemberConverter,
                                  command,
                                  cooldown)
from discord.ext.tasks import loop

from classes.TwitchClient import TwitchClient
from config.embed.activity import activity_config
from config.embed.hello import hello_config
from config.embed.pfp import pfp_config
from config.embed.playing_act import playing_activity_config
from config.embed.spotify import spotify_config
from config.embed.streaming_act import streaming_activity_config
from config.main import PREFIX
from functions.embed_factory import create_embed
from functions.find_gif import find_gif
from functions.get_twitch_user import get_twitch_user_pfp
from util.twitch_bearer import twitch_bearer


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
        aliases=["pfp"])
    @cooldown(1, 5, BucketType.user)
    async def pfp(self, ctx: Context, member: MemberConverter = None):

        member = member or ctx.author

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
    @cooldown(1, 7, BucketType.user)
    async def status(self, ctx: Context, member: MemberConverter = None) -> None:

        member = member or ctx.author

        if not member.activities:
            if member == ctx.author:
                await ctx.message.reply("https://pics.me.me/thumb_c-mon-do-something-me-irl-38375559.png")
            else:
                await ctx.send(f"{member.mention}")
                await ctx.send("https://pics.me.me/thumb_c-mon-do-something-me-irl-38375559.png")
            return

        acts = member.activities

        if all(isinstance(e, CustomActivity) for e in acts):

            if member == ctx.author:
                await ctx.message.reply("Try again later with someone who's actually doing something, "
                                        "not a snob like you wasting his life energy instead of being a "
                                        "useful human being... 🙄")
            else:
                await ctx.send(f"{member.mention} Go listen to some music or do something in your life 🙄")
            return

        act = (acts[1:])[0] if len(acts) > 1 else acts[0]

        config: dict = {}

        match act:
            case Spotify():
                async with ctx.typing():
                    config = spotify_config(
                        member.mention,
                        act.title,
                        act.album,
                        act.artist,
                        act.album_cover_url,
                        f"https://open.spotify.com/track/{act.track_id}")

            case Game():
                async with ctx.typing():
                    config = playing_activity_config(
                        act.name,
                        member.mention,
                        ctx.author,
                        ctx.message.author.avatar_url,
                        act.start.strftime('%x %X') if act.start else None
                    )

            case Streaming():
                async with ctx.typing():
                    streamer_image_url: str | None = await get_twitch_user_pfp(act.url[22:])

                    if not streamer_image_url.startswith("https://"):
                        streamer_image_url = None

                    config = streaming_activity_config(
                        act.name,
                        member.mention,
                        ctx.author,
                        ctx.message.author.avatar_url,
                        act.platform,
                        stream_url=act.url,
                        streamed_game=act.game,
                        streamer_pfp=streamer_image_url
                    )

            case Activity():
                async with ctx.typing():
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

    @loop(hours=24, reconnect=True)
    async def decrement_token_validity(self):

        TwitchClient().decrement_expiration()

    @decrement_token_validity.before_loop
    async def before_token_decrement(self):
        
        TwitchClient(await twitch_bearer())

        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(UserCog(bot))
