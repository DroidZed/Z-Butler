from typing import Optional

from discord import (
    Spotify,
    Game,
    Streaming,
    Activity,
    CustomActivity,
    Member,
    User,
)
from discord.ext.commands import (
    Bot,
    BucketType,
    Cog,
    Context,
    command,
    cooldown,
)
from discord.ext.tasks import loop

from utils import Env

from modules.embedder import generate_embed
from modules.tenor_api import TenorAPI
from modules.twitching import (
    TwitchClient,
    authenticate,
    get_pfp,
)


class UserCog(
    Cog,
    name="User-Commands",
    description="👤 User commands for everyone",
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.tenor_api = TenorAPI()

    #    self.decrement_token_validity.start()

    def cog_unload(self):
        self.decrement_token_validity.stop()

    @command(
        name="pic",
        usage=f"{Env.PREFIX}pic `username`",
        description="Display the requested user's profile picture.",
        aliases=["pfp"],
    )
    @cooldown(1, 5, BucketType.user)
    async def pfp(
        self,
        ctx: Context,
        member: User | Member | None = None,
    ):
        member = member or ctx.author

        await ctx.send(
            embed=generate_embed(
                title=f"**{'Lord  👑 **𝕯𝖗𝖔𝖎𝖉𝖅𝖊𝖉** 👑' if member.id == Env.CROWN_ROLE_ID else f'{member.display_name}#{member.discriminator}'}**'s Profile Picture",
                color=Env.BOT_COLOR,
                image_url=f"{member.avatar.url if member.avatar else ''}",
                footer_text=f"Requested by {ctx.message.author} 💙",
                footer_icon=f"{ctx.message.author.avatar.url if ctx.message.author.avatar else ''}",
            )
        )

    @command(
        name="greet",
        usage=f"{Env.PREFIX}greet `username`",
        description="Greet a given user",
        aliases=["grt"],
    )
    @cooldown(1, 3, BucketType.user)
    async def hello(
        self,
        ctx: Context,
        *,
        member: User | Member | None = None,
    ):
        member = member or ctx.author

        await ctx.message.delete()

        async with ctx.typing():
            link = await self.tenor_api.find_gif("Hello")

            if not isinstance(link, str):
                link = "https://tenor.com/view/0001-gif-25597406"

        await ctx.send(
            embed=generate_embed(
                title="Z Butler's Greeting",
                color=Env.BOT_COLOR,
                description=f"Hello <@{member.id}>~ 👋🏻",
                image_url=link,
            )
        )

    @command(
        name="status",
        description="Get the status of a user, can be either a `song`, a `game`, a `stream` or any `custom "
        "activity`.\n Ignoring the bio.",
        usage=f"{Env.PREFIX}status `username`",
        aliases=["st?"],
    )
    @cooldown(1, 7, BucketType.user)
    async def status(
        self,
        ctx: Context,
        member: User | Member | None = None,
    ):
        member = member or ctx.author
        acts = member.activities  # type: ignore

        def change_platform_color(platform: str):
            match platform:
                case "Twitch":
                    return Env.TWITCH_PURPLE
                case "YouTube":
                    return Env.YOUTUBE_RED
                case _:
                    return Env.BOT_COLOR

        def resolve_desc(
            stream_url: Optional[str],
            streamed_game: Optional[str],
            platform: str,
            desc: str,
        ):
            if stream_url:
                desc += f"\nFollow this [link]({stream_url}) to catch them **LIVE** 🔴 on `{platform}` !"

            if streamed_game:
                desc = desc.replace(
                    "this", f"{streamed_game}"
                )

            return desc

        def resolve_image_url(image_url: Optional[str]):
            return (
                image_url
                if image_url
                else "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
            )

        if not acts:
            if member == ctx.author:
                return await ctx.message.reply(
                    "https://pics.me.me/thumb_c-mon-do-something-me-irl-38375559.png",
                    mention_author=True,
                )
            else:
                return await ctx.send(
                    f"{member.mention}\nhttps://pics.me.me/thumb_c-mon-do-something-me-irl-38375559.png"
                )

        if all(isinstance(e, CustomActivity) for e in acts):
            if member == ctx.author:
                return await ctx.message.reply(
                    "Try again later with someone who's actually doing something, "
                    "not a snob like you wasting his life energy instead of being a "
                    "useful human being... 🙄",
                    mention_author=True,
                )
            else:
                return await ctx.send(
                    f"{member.mention} Go listen to some music or do something in your life 🙄"
                )

        act = (acts[1:])[0] if len(acts) > 1 else acts[0]

        match act:
            case Spotify():
                async with ctx.typing():
                    embed = generate_embed(
                        title=f"**{act.title}**",
                        color=Env.SPOTIFY_COLOR,
                        description=f"{member.mention} is listening to this song by _{act.artist}_\nFrom the album **{act.album}**.\n Check it out -> [link](https://open.spotify.com/track/{act.track_id})",
                        image_url=act.album_cover_url,
                        footer_text="Songs params provided by Spotify 💚",
                        footer_icon="https://1000logos.net/wp-content/uploads/2017/08/Spotify-Logo.png",
                    )
                return await ctx.send(embed=embed)

            case Game():
                async with ctx.typing():
                    embed = generate_embed(
                        title=f"{act.name}",
                        description=f"{member.mention} has been `playing` ***{act.name}*** since {act.start.strftime('%x %X') if act.start else ''} 🎮",
                        color=Env.BOT_COLOR,
                        footer_text=f"Requested by {ctx.author} 💙",
                        footer_icon=f"{ctx.message.author.display_avatar.url}",
                    )

                return await ctx.send(embed=embed)

            case Streaming():
                async with ctx.typing():
                    streamer_image_url: str | None = (
                        await get_pfp(act.url[22:])
                    )

                    if (
                        streamer_image_url
                        and not streamer_image_url.startswith(
                            "https://"
                        )
                    ):
                        streamer_image_url = None

                    embed = generate_embed(
                        title=act.name,
                        description=resolve_desc(
                            act.url,
                            act.game,
                            act.platform,  # type: ignore
                            f"{member.mention} is `streaming` ***this*** 👻",
                        ),
                        image_url=streamer_image_url,
                        color=change_platform_color(
                            act.platform  # type: ignore
                        ),
                        url=f"{act.url}",
                        footer_text=f"Requested by {ctx.author} 💙",
                        footer_icon=f"{ctx.message.author.display_avatar.url}",
                    )
                return await ctx.send(embed=embed)

            case Activity():
                async with ctx.typing():
                    embed = generate_embed(
                        title=f"{member.display_name}'s Activity",
                        description=f"{act.name} since {act.start.strftime('%x %X') if act.start else ''}",
                        image_url=resolve_image_url(
                            act.large_image_url
                        ),
                        color=Env.BOT_COLOR,
                        footer_text=f"Requested by {ctx.author} 💙",
                        footer_icon=ctx.message.author.display_avatar.url,
                    )
                return await ctx.send(embed=embed)
            case _:
                return await ctx.send(
                    "Nothing, move along...."
                )

    @loop(hours=24, reconnect=True)
    async def decrement_token_validity(self):
        TwitchClient().decrement_expiration()

    @decrement_token_validity.before_loop
    async def before_token_decrement(self):
        TwitchClient(await authenticate())

        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(UserCog(bot))
