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
        name="dragons",
        usage=f"{Env.PREFIX}dragons",
        description="Gives info about Elder Scrolls Dragons Dragons",
    )
    @cooldown(1, 2.5, BucketType.user)
    async def dragons(self, ctx: Context):
        await ctx.send(
            embed=generate_embed(
                title="Elder Scrolls Dragons Info",
                description="Use this command to inform yourself about the mysterious creatures tha tear the skies of Mundus, SoulCairn and Sovngarde!.",
            )
        )


def setup(bot: Bot):
    bot.add_cog(TheElderScrolls(bot))
