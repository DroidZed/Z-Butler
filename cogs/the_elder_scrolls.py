from discord.ext.commands import (
    Bot,
    BucketType,
    Cog,
    Context,
    command,
    cooldown,
)

from utils import Env

from modules.embedder import generate_embed


class TheElderScrolls(
    Cog,
    name="The Elder Scrolls[WIP]",
    description="Everything about The Elder Scrolls",
):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="sky_drags",
        usage=f"{Env.PREFIX}sky_drags",
        description="Gives info about Skyrim Dragons",
        alises=["skds"],
    )
    @cooldown(1, 2.5, BucketType.user)
    async def skyrim_dragons(self, ctx: Context):
        await ctx.send(
            embed=generate_embed(
                title="Skyrim Dragons Info",
                description="Use this command to inform yourself about the mysterious creatures tha tear the northern skies of Skyrim.",
            )
        )


def setup(bot: Bot):
    bot.add_cog(TheElderScrolls(bot))
