from config.main import PREFIX
from discord.ext.commands import (Bot, BucketType, Cog, Context, command,
                                  cooldown)


class MusicCog(Cog,
               name="Music Category",
               description="Enjoy the bits and pieces of the music you like."
               ):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="lycris",
        description="Gives the lyrics of a requested song.",
        usage=f"{PREFIX}lyrics <song name>",
        aliases=['ly?']
    )
    @cooldown(1, 5, BucketType.user)
    async def lyrics(self, ctx: Context, *title: str) -> None:
        await ctx.send(f'You searched for {" ".join(title)}.')

    @command(
        name="song?",
        description="Looks for a perticular song.",
        usage=f"{PREFIX}song? <song name>"
    )
    @cooldown(1, 5, BucketType.user)
    async def search_song(self, ctx: Context, *title: str) -> None:
        await ctx.send(f'You searched for {" ".join(title)}.')


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
