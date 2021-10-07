from asyncio import sleep

from discord import Message, Reaction, Member
from discord.ext.commands import (Bot,
                                  BucketType,
                                  Cog,
                                  Context,
                                  command,
                                  cooldown)
from discord.ext.tasks import loop

from config.embed.quote import quotes_config
from config.main import PREFIX
from functions.embed_factory import create_embed
from functions.quotes_api import quotes_gql


async def _grab_quote():
    api = await quotes_gql()

    return api['randomQuote']


class QuotesCog(Cog, name="Quotes Category", description="Quoty quotes !"):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.daily_quote.start()

    def cog_unload(self):
        self.daily_quote.stop()

    @command(
        name="quote",
        description="Get a random quote",
        usage=f"{PREFIX}q?",
        aliases=['q?'])
    @cooldown(1, 5, BucketType.user)
    async def random_quote(self, ctx: Context) -> None:
        async with ctx.typing():
            quote = await _grab_quote()

        msg: Message = await ctx.send(embed=create_embed(quotes_config(quote['author'], quote['body'])))

        await sleep(1)

        await msg.add_reaction("💖")

        def check(reaction: Reaction, user: Member):
            return user == ctx.author and str(reaction.emoji) in ["💖"] and reaction.message == msg

        confirmation = await self.bot.wait_for("reaction_add", check=check)

        if confirmation:
            await ctx.author.send(embed=msg.embeds[0])

    @loop(hours=24, reconnect=True)
    async def daily_quote(self) -> None:

        quote = await _grab_quote()

        await self.bot.get_channel(696838753528053782).send(
            embed=create_embed(
                quotes_config(
                    quote['author'],
                    quote['body']
                )
            )
        )

    @daily_quote.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(QuotesCog(bot))
