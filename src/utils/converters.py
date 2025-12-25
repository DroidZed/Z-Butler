from discord.ext.commands import Converter


class SongMetadataConverter(Converter):
    async def convert(self, ctx, argument):
        if not argument or len(argument) == 0:
            return ""

        return argument.replace("_", " ")


class SongArtistConverter(SongMetadataConverter):
    pass


class SongNameConverter(SongMetadataConverter):
    pass
