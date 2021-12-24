from discord.ext.commands import Converter


class SongArtistConverter(Converter):

    async def convert(self, ctx, argument):

        if not argument or len(argument) == 0:
            return

        return argument.replace("_", " ")


class SongNameConverter(Converter):

    async def convert(self, ctx, argument):

        if not argument or len(argument) == 0:
            return

        return argument.replace("_", " ")
