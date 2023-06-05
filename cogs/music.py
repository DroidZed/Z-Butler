from typing import Optional

from discord import Spotify, Forbidden
from discord.ext.commands import (
    Bot,
    BucketType,
    Cog,
    Context,
    command,
    cooldown,
)

from config import Env
from modules.melody_wave import MelodyWave, Wave
from modules.embedder import generate_embed
from utils.converters import SongNameConverter, SongArtistConverter


class MusicCog(
    Cog,
    name="Muse",
    description="🎶 Enjoy the bits and pieces of the music you like.",
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.melo = MelodyWave()

    async def __send_lyrics(
        self, ctx: Context, title: str, artist: str
    ) -> None:
        if not (title and artist):
            await ctx.send("❌ invalid input !!")
            return

        async with ctx.typing():
            data = await self.melo.fetch_lyrics(
                title, artist
            )

        if not isinstance(data, Wave):
            await ctx.send(
                "❌ Cannot find lyrics for the given song...."
            )
            return

        else:
            try:
                await ctx.author.send(
                    embed=generate_embed(
                        title=f"**{data.title}** by {data.artist}",
                        url=data.song_url,
                        color=Env.BOT_COLOR,
                        description=(
                            f"The lyrics were too long, here's a [link instead]({data.song_url})."
                            if len(data.lyrics) > 4096
                            else data.lyrics
                        ),
                        image_url=f"{data.art_url}",
                        thumbnail_url=Env.SERVER_IMAGE,
                        footer_text="Lyrics by Genius Lyrics 💙",
                        footer_icon="https://crypttv.com/wp-content/uploads/2020/10/59-598221_genius-lyrics-logo-transparent-clipart.png",
                    )
                )
            except Forbidden:
                await ctx.reply(
                    "Please open your DMs to get the lyrics !!",
                    mention_author=True,
                )

    @command(
        name="lyrics",
        description="Give the lyrics of a requested song."
        "\nYou can also use the song you're currently listening to on Spotify."
        "To achieve that, simply run the command without arguments."
        "\n**DISCLAIMER**: not all songs are supported.",
        usage=f"{Env.PREFIX}lyrics `song_name` (respect the _ !) `song_artist` | Nothing",
        aliases=["ly?"],
    )
    @cooldown(1, 5, BucketType.user)
    async def lyrics(
        self,
        ctx: Context,
        title: Optional[SongNameConverter] = None,
        artist: Optional[SongArtistConverter] = None,
    ) -> None:
        if not title and not artist:
            acts = ctx.author.activities

            act = None

            raw_title, raw_artist = "", ""

            for a in acts:
                if isinstance(a, Spotify):
                    act = a

            if isinstance(act, Spotify):
                raw_title = act.title
                raw_artist = act.artist

        await self.__send_lyrics(ctx, raw_title, raw_artist)

    @command(
        name="song",
        description="Looks for a particular song.",
        usage=f"{Env.PREFIX}song `song_name` (respect the _ !) `song_artist`",
        aliases=["sg?"],
    )
    @cooldown(1, 5, BucketType.user)
    async def search_song(
        self,
        ctx: Context,
        title: SongNameConverter,
        artist: SongArtistConverter,
    ) -> None:
        async with ctx.typing():
            data = find_song(title, artist)

        if not data:
            await ctx.send(
                "❌ Unable to find the song you're looking for...Try again later."
            )
            return

        await ctx.send(
            embed=EmbedFactory.create_embed(
                EmbedFactory.create_config(
                    title=f"**{data['track']}**",
                    url=data["href"],
                    color=Env.SPOTIFY_COLOR,
                    description=f"The song you've requested, by {' '.join(art for art in data['artists'])} from the "
                    f"album **{data['album']['name']}**",
                    image={
                        "url": f"{data['album']['art']['url']}",
                        "width": data["album"]["art"][
                            "width"
                        ],
                        "height": data["album"]["art"][
                            "height"
                        ],
                    },
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586"
                        "/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={"url": Env.SERVER_IMAGE},
                    footer={
                        "text": "Songs params provided by Spotify 💚",
                        "icon_url": "https://1000logos.net/wp-content/uploads/2017/08/Spotify-Logo.png",
                    },
                )
            )
        )


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
