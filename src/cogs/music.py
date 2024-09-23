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


from modules.melody_wave import MelodyWave, Wave, Melody
from modules.embedder import generate_embed
from utils import (
    Env,
    SongNameConverter,
    SongArtistConverter,
)


class MusicCog(
    Cog,
    name="Muse",
    description="🎶 Enjoy the bits and pieces of the music you like.",
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.melo = MelodyWave()

    async def __send_lyrics(self, ctx: Context, title: str, artist: str):
        if not (title and artist):
            return await ctx.send("❌ invalid input !!")

        async with ctx.typing():
            data = await self.melo.fetch_lyrics(title, artist)

        if not isinstance(data, Wave):
            return await ctx.send("❌ Cannot find lyrics for the given song....")

        else:
            try:
                await ctx.author().send(
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
                return await ctx.reply(
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
    ):
        if not title and not artist:
            raw_title, raw_artist = "", ""
            acts = ctx.author().activities  # type: ignore

            for a in acts:
                if isinstance(a, Spotify):
                    raw_title = a.title
                    raw_artist = a.artist

            return await self.__send_lyrics(ctx, raw_title, raw_artist)
        return await self.__send_lyrics(ctx, title, artist)  # type: ignore

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
    ):
        async with ctx.typing():
            result = await self.melo.search_song(title, artist)  # type: ignore

            match result:
                case Melody():
                    embed = generate_embed(
                        title=f"**{result.track}**",
                        url=result.href,
                        color=Env.SPOTIFY_COLOR,
                        description=f"The song you've requested, by {' '.join(art for art in result.artists)} from the "
                        f"album **{result.album.name}**",
                        image_url=f"{result.album.art}",
                        thumbnail_url=Env.SERVER_IMAGE,
                        footer_icon="https://1000logos.net/wp-content/uploads/2017/08/Spotify-Logo.png",
                        footer_text="Songs params provided by Spotify 💚",
                    )
                    return await ctx.send(embed=embed)

                case _:
                    return await ctx.send(
                        "❌ Unable to find the song you're looking for...Try again later."
                    )


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
