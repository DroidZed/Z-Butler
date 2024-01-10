from discord import TextChannel

from discord.ext.commands import (
    Bot,
    BucketType,
    Cog,
    Context,
    command,
    cooldown,
    is_owner,
)

from discord.ext.tasks import loop

from modules.japan_heaven.anime_quoter import AnimeQuote

from utils import Env
from modules.japan_heaven import AnimeQuoter
from modules.embedder import (
    generate_embed,
)


async def _grab_quote():
    return await AnimeQuoter().random_anime_quote()


# FIXME: Find what happened to the quotes API !
class QuotesCog(
    Cog, name="Quotes", description="💭 Quoty quotes !"
):
    def __init__(self, bot: Bot):
        self.bot = bot

    def cog_unload(self):
        self.daily_quote.stop()

    async def _send_quote(
        self, destination: Context, quote: AnimeQuote
    ):
        await destination.send(
            embed=generate_embed(
                title=f"**{quote.character} - {quote.anime}**",
                color=Env.BOT_COLOR,
                description=f"*{quote.quote}*",
            )
        )

    @command(
        name="quote",
        description="Get a random quote",
        usage=f"{Env.PREFIX}q?",
        aliases=["q?"],
    )
    @cooldown(1, 5, BucketType.user)
    async def random_quote(self, ctx: Context):
        async with ctx.typing():
            result = await _grab_quote()

            match result:
                case AnimeQuote():
                    return await self._send_quote(
                        ctx, result
                    )
                case _:
                    return await ctx.send(
                        embed=generate_embed(
                            title="Quote - Error",
                            description="No quotes for you...",
                            color=Env.BOT_COLOR,
                        )
                    )

    @command(
        name="sdq",
        description="Starts the daily quote task.",
        usage=f"{Env.PREFIX}sdq",
    )
    @is_owner()
    async def start_daily_quotes(self, ctx: Context):
        try:
            await ctx.send(
                "🏃 Starting the daily quote routine...",
                delete_after=1.5,
            )
            self.daily_quote.start()
        except RuntimeError:
            return await ctx.send(
                embed=generate_embed(
                    title="Quoty - Error",
                    description="Task already started!",
                )
            )

    @command(
        name="!sdq",
        description="Stops the daily quote task.",
        usage=f"{Env.PREFIX}!sdq",
    )
    @is_owner()
    async def stop_daily_quotes(self, ctx: Context):
        try:
            await ctx.send(
                embed=generate_embed(
                    title="Quoty",
                    description="🛑 Ending the daily quote routine...",
                ),
                delete_after=1.5,
            )
            self.daily_quote.cancel()
        except RuntimeError:
            return await ctx.send(
                embed=generate_embed(
                    title="Quoty - Error",
                    description="Task already cancelled!",
                )
            )

    @loop(hours=24, reconnect=True)
    async def daily_quote(self):
        result = await _grab_quote()

        wisdom_channel = self.bot.get_channel(
            1071141767145082910
        )

        if wisdom_channel and isinstance(
            wisdom_channel, TextChannel
        ):
            match result:
                case AnimeQuote():
                    return await wisdom_channel.send(
                        embed=generate_embed(
                            title=f"**{result.character} - {result.anime}**",
                            color=Env.BOT_COLOR,
                            description=f"*{result.quote}*",
                        )
                    )
                case _:
                    return await wisdom_channel.send(
                        embed=generate_embed(
                            title="Quoty",
                            description="No quotes for now...",
                        )
                    )

    @daily_quote.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(QuotesCog(bot))
