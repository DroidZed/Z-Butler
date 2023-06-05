from re import compile

from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
    cooldown,
    BucketType,
)

from utils import Env

from coinpaprika_async import Client


class Miscellaneous(
    Cog,
    name="Miscellaneous [WIP]",
    description="Useful commands for the average user...WORK IN "
    "PROGRESS, not fully implemented YET !!",
):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="convert",
        usage=f"{Env.PREFIX}convert `base` `amount` `target`",
        description="""
             Converts the amount into the corresponding currency. Only abbreviations are supported.
             Here's a decent list including a large amount of acronyms to use with this command,
             find it [here](https://infomediang.com/cryptocurrency-abbreviations/).
             """,
        aliases=["conv"],
    )
    @cooldown(1, 4.7, BucketType.user)
    async def crypto_converter(
        self, ctx: Context, *currency_message: str
    ):
        msg = " ".join(currency_message)

        rgx = compile(
            "([a-zA-Z ]*?) ([\\d.]+) ([a-zA-Z ]+)"
        )

        res = rgx.match(msg)

        if not res:
            await ctx.send("❌ Invalid input !!")
            return

        base = res.groups()[0]
        amount = float(res.groups()[1])
        target = res.groups()[2]

        client = Client()

        res = await client.price_converter(
            {
                "base_currency_id": base,
                "quote_currency_id": target,
                "amount": amount,
            }
        )

        if res.status_code >= 400:
            return await ctx.send(
                "An error occurrent when converting the coins!"
            )

        await ctx.send(
            f"You're converting {amount} {base}(s) into {target}(s).\nFinal value is {res.data}"
        )


def setup(bot: Bot):
    bot.add_cog(Miscellaneous(bot))
