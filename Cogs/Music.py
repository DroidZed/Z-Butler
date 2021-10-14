from typing import Optional

from discord import Member, Spotify
from discord.ext.commands import (Bot, BucketType, Cog, Context, command,
                                  cooldown)

from config.embed.lyrics import lyrics_config
from config.embed.song import song_config
from config.main import PREFIX
from functions.embed_factory import create_embed
from functions.lyrics import query_lyrics
from functions.spotify_search import spotify_search_rest


def _parse_metadata(*info: str) -> Optional[tuple[str, str]]:
    if not info or len(info) <= 1:
        return None

    metadata = " ".join(info).split(" ")

    metadata.remove(info[0])

    title = info[0].replace("_", " ")

    artist = " ".join(metadata)

    return title, artist


async def _send_lyrics(ctx, title: str, artist: str) -> None:
    async with ctx.typing():
        data = query_lyrics(title, artist)

    if not data["valid"]:

        await ctx.send("❌ Cannot find lyrics for the given song....")
        return

    else:

        emb = create_embed(
            lyrics_config(**data),
            None,
            None
        )

        if len(emb.description) > 4096:
            emb.description = f"The lyrics were too long, here's a [link instead]({data['song_url']})."

        await ctx.send(f'{ctx.author.mention}, check your inbox !!', delete_after=10)
        await ctx.author.send(embed=emb)


class MusicCog(Cog,
               name="🎶 Music Category",
               description="Enjoy the bits and pieces of the music you like."
               ):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="lyrics",
        description="Give the lyrics of a requested song.\nYou can also, if you want, use the song you're currently "
                    "listening to on Spotify. To achieve that, simply run the command without arguments",
        usage=f"{PREFIX}lyrics `song_name` (respect the _ !) `artist` | Nothing",
        aliases=['ly?']
    )
    @cooldown(1, 5, BucketType.user)
    async def lyrics(self, ctx: Context, *info: str) -> None:

        if not info or len(info) <= 1:

            member: Member = ctx.author

            acts = member.activities

            act = (acts[1:])[0] if len(acts) > 1 else acts[0]

            if isinstance(act, Spotify):
                await _send_lyrics(ctx, act.title, act.artist)
                return
        else:

            try:
                title, artist = _parse_metadata(*info)
            except TypeError:
                await ctx.send("Invalid args !")
                return

            await _send_lyrics(ctx, title, artist)

    @command(
        name="song",
        description="Looks for a particular song.",
        usage=f"{PREFIX}song `song_name` (respect the _ !) `artist`"
    )
    @cooldown(1, 5, BucketType.user)
    async def search_song(self, ctx: Context, *info: str) -> None:

        try:
            title, artist = _parse_metadata(*info)
        except TypeError:
            await ctx.send("Invalid args !")
            return

        async with ctx.typing():

            res = spotify_search_rest(title, artist)

        if res:

            await ctx.send(embed=create_embed(
                song_config(**res),
                None,
                None
                )
            )

        else:
            await ctx.send("Could not find the song you're looking for ! Try again later.")


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
