from re import compile

from discord.ext.commands import Bot, Cog, Context, command, cooldown, BucketType

from config.main import PREFIX


class Miscellaneous(
    Cog,
    name="Miscellaneous [WIP]",
    description="Useful commands for the average user...WORK IN " "PROGRESS, not fully implemented YET !!",
):
    def __init__(self, bot: Bot):

        self.bot = bot

    @command(
        name="convert",
        usage=f"{PREFIX}convert `base` `amount` `target`",
        description="""
             Converts the amount into the corresponding currency. Only abbreviations are supported.
             Here's a decent list including a large amount of acronyms to use with this command,
             find it [here](https://infomediang.com/cryptocurrency-abbreviations/).
             """,
        aliases=["conv"],
    )
    @cooldown(1, 4.7, BucketType.user)
    async def crypto_converter(self, ctx: Context, *currency_message: str):

        currency_message = " ".join(currency_message)

        rgx = compile("([a-zA-Z ]*?) ([0-9.0-9]+) ([a-zA-Z ]+)")

        res = rgx.match(currency_message)

        if not res:
            await ctx.send("❌ Invalid input !!")
            return

        base, amount, target = res.groups()

        await ctx.send(f"You're converting {amount} {base}(s) into {target}(s).")


def setup(bot: Bot):

    bot.add_cog(Miscellaneous(bot))
