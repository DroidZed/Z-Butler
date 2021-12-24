from discord.ext.commands import (Bot,
                                  Cog, Context, command, cooldown, BucketType)

from config.main import PREFIX


class Miscellaneous(Cog, name="Miscellaneous [WIP]", description="Useful commands for the average user...WORK IN "
                                                                 "PROGRESS, not fully implemented YET !!"):

    def __init__(self, bot: Bot):

        self.bot = bot

    @command(name="crypt",
             usage=f"{PREFIX}crypt `amount` `currency 1` `currency 2`",
             description="Converts the amount into ",
             aliases=["exchg"])
    @cooldown(1, 4.7, BucketType.user)
    async def crypto_converter(self, ctx: Context, amount: float, currency_start: str, currency_end: str):

        await ctx.send(f"You're converting {amount} from {currency_start} into {currency_end}. ")


def setup(bot: Bot):

    bot.add_cog(Miscellaneous(bot))
