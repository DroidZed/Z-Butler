from discord.ext.commands import Bot, BucketType, Cog, Context, command, cooldown

from classes.embed_factory import EmbedFactory
from config.main import PREFIX


class TheElderScrolls(Cog, name="The Elder Scrolls[WIP]", description="Everything about The Elder Scrolls"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="sky_drags", usage=f"{PREFIX}sky_drags", description="Gives info about Skyrim Dragons", alises=["skds"]
    )
    @cooldown(1, 2.5, BucketType.user)
    async def skyrim_dragons(self, ctx: Context):
        await ctx.send(
            embed=EmbedFactory.create_embed(
                EmbedFactory.create_config(
                    title="Skyrim Dragons Info",
                    description="Use this command to inform yourself about the mesterious cratures tha tear the Northern skyies of Skyrim.",
                )
            )
        )


def setup(bot: Bot):
    bot.add_cog(TheElderScrolls(bot))
