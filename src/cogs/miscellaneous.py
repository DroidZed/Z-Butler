import asyncio
from genericpath import isfile
import os
from re import compile

from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
    cooldown,
    BucketType,
)

from discord import FFmpegPCMAudio, Forbidden, Member, HTTPException, VoiceState
from gtts import gTTS

from coinpaprika_async_client import ApiError

from modules.embedder.embedder_machine import generate_embed
from utils import Env
from modules.views import LangSelect


from modules.coinpaprika import CoinManager


class Miscellaneous(
    Cog,
    name="Miscellaneous [WIP]",
    description="Useful commands for the average user...WORK IN "
    "PROGRESS, not fully implemented YET !!",
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.coin_manager = CoinManager()

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
    async def crypto_converter(self, ctx: Context, *currency_message: str):
        msg = " ".join(currency_message)

        rgx = compile("([a-zA-Z ]*?) ([\\d.]+) ([a-zA-Z ]+)")

        res = rgx.match(msg)

        if not res:
            await ctx.send("❌ Invalid input !!")
            return

        base = res.groups()[0]
        amount = int(res.groups()[1])
        target = res.groups()[2]

        res = await self.coin_manager.convert_coin(
            base,
            target,
            amount,
        )

        if isinstance(res, ApiError):
            return await ctx.send(
                "An error occurrent when converting the coins!"
            )

        await ctx.send(
            f"You're converting {amount} {base}(s) into {target}(s).\nFinal value is {res.price}"
        )


def setup(bot: Bot):
    bot.add_cog(Miscellaneous(bot))
