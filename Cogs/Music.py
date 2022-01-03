from discord import Spotify
from discord.ext.commands import (Bot, BucketType, Cog, Context, command,
                                  cooldown)

from classes.SongMetadataConverter import SongArtistConverter, SongNameConverter
from config.embed.lyrics import lyrics_config
from config.embed.song import song_config
from config.main import PREFIX
from functions.embed_factory import create_embed
from functions.lyrics import query_lyrics
from functions.spotify_search import spotify_search_rest


async def _send_lyrics(ctx, title: str, artist: str) -> None:

    async with ctx.typing():
        data = query_lyrics(title, artist)

    if not data["valid"]:

        await ctx.send("❌ Cannot find lyrics for the given song....")
        return

    emb = create_embed(lyrics_config(**data), None, None)

    if len(emb.description) > 4096:
        emb.description = f"The lyrics were too long, here's a [link instead]({data['song_url']})."

    await ctx.send(f'{ctx.author.mention}, check your inbox !!', delete_after=10)
    await ctx.author.send(embed=emb)


class MusicCog(Cog,
               name="Muse",
               description="🎶 Enjoy the bits and pieces of the music you like."):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="lyrics",
        description="Give the lyrics of a requested song.\nYou can also if you want, use the song you're currently "
                    "listening to on Spotify."
                    "To achieve that, simply run the command without arguments.",
        usage=f"{PREFIX}lyrics `song_name` (respect the _ !) `song_artist` | Nothing",
        aliases=['ly?']
    )
    @cooldown(1, 5, BucketType.user)
    async def lyrics(self, ctx: Context, title: SongNameConverter = None, artist: SongArtistConverter = None) -> None:

        if not title and not artist:

            acts = ctx.author.activities

            act = (acts[1:])[0] if len(acts) > 1 else acts[0]

            if isinstance(act, Spotify):
                title = act.title
                artist = act.artist

        await _send_lyrics(ctx, title, artist)

    @command(
        name="song",
        description="Looks for a particular song.",
        usage=f"{PREFIX}song `song_name` (respect the _ !) `song_artist`",
        aliases=['sg?']
    )
    @cooldown(1, 5, BucketType.user)
    async def search_song(self, ctx: Context, title: SongNameConverter, artist: SongArtistConverter) -> None:

        async with ctx.typing():

            res = spotify_search_rest(title, artist)

        if not res:

            await ctx.send("❌ Unable to find the song you're looking for...Try again later.")
            return

        await ctx.send(embed=create_embed(song_config(**res), None, None))

    @lyrics.error
    async def lyrics_handler(self, ctx: Context):

        await ctx.send("❌ Oops...command error, better luck next time !")


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
