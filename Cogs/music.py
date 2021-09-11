from discord.ext.commands import (Bot, BucketType, Cog, Context, command,
                                  cooldown)

from config.embed.lyrics import lyrics_config
from config.embed.song import song_config
from config.main import PREFIX
from functions.embed_factory import create_embed
from functions.lyrics import query_lyrics
from functions.song import look_for_song


def _parse_metadata(*info: str):

    if not info:
        return None

    metadata = " ".join(info).split(" ")

    metadata.remove(info[0])

    title = info[0].replace("_", " ")

    artist = " ".join(m for m in metadata)

    return title, artist


class MusicCog(Cog,
               name="Music Category",
               description="Enjoy the bits and pieces of the music you like."
               ):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="lyrics",
        description="Gives the lyrics of a requested song.",
        usage=f"{PREFIX}lyrics `song_name` (respect the _ !) `artist`",
        aliases=['ly?']
    )
    @cooldown(1, 5, BucketType.user)
    async def lyrics(self, ctx: Context, *info: str) -> None:

        try:
            title, artist = _parse_metadata(*info)
        except TypeError:
            await ctx.send("Invalid args !")
            return

        async with ctx.typing():
            data = query_lyrics(title, artist)

        if data["valid"]:

            await ctx.send(f'{ctx.author.mention}, check your inbox !!', delete_after=10)
            await ctx.author.send(embed=create_embed(
                    lyrics_config(**data),
                    None,
                    None
                )
                )

        else:
            await ctx.send("Could not find the song you're looking for ! Try again later.")

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
            data = look_for_song(title, artist)

        if data["valid"]:

            await ctx.send(embed=create_embed(
                song_config(**data),
                None,
                None
            )
            )

        else:
            await ctx.send("Could not find the song you're looking for ! Try again later.")


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
