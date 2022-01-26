from asyncio import sleep

from discord import Message, Reaction, Member
from discord.ext.commands import Bot, BucketType, Cog, Context, command, cooldown
from discord.ext.commands.core import has_role
from discord.ext.commands.errors import CommandError, MissingRole
from discord.ext.tasks import loop

from api.anime_quotes import anime_quotes
from config.embed.quote import quotes_config
from config.main import PREFIX, CROWN_ROLE_ID
from functions.embed_factory import create_embed


async def _grab_quote():
    return await anime_quotes()


class QuotesCog(Cog, name="Quotes", description="💭 Quoty quotes !"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.daily_quote.start()

    def cog_unload(self):
        self.daily_quote.stop()

    @command(
        name="quote",
        description="Get a random quote",
        usage=f"{PREFIX}q?",
        aliases=["q?"],
    )
    @cooldown(1, 5, BucketType.user)
    async def random_quote(self, ctx: Context):
        async with ctx.typing():
            quote = await _grab_quote()

        msg: Message = await ctx.send(
            embed=create_embed(quotes_config(f"{quote['character']} - {quote['anime']}", quote["quote"]))
        )

        await sleep(1)

        await msg.add_reaction("💖")

        def check(reaction: Reaction, user: Member):
            return user == ctx.author and str(reaction.emoji) in ["💖"] and reaction.message == msg

        confirmation = await self.bot.wait_for("reaction_add", check=check)

        if confirmation:
            await ctx.author.send(embed=msg.embeds[0])

    @command(name="sdq", description="Starts the daily quote task.", usage=f"{PREFIX}sdq")
    @has_role(CROWN_ROLE_ID)
    async def start_daily_quotes(self, ctx: Context):
        await ctx.send("🏃 Starting the daily quote routine...", delete_after=1.5)
        self.daily_quote.start()

    @command(name="!sdq", description="Stops the daily quote task.", usage=f"{PREFIX}!sdq")
    @has_role(CROWN_ROLE_ID)
    async def stop_daily_quotes(self, ctx: Context):
        await ctx.send("🛑 Ending the daily quote routine...", delete_after=1.5)
        self.daily_quote.cancel()

    @stop_daily_quotes.error
    async def stop_daily_quotes_handler(self, ctx: Context, error: CommandError):

        if isinstance(error, MissingRole):
            await ctx.send(
                "Get a life you stupid fat fuck, talk to real life people instead of wasting my time, "
                "you're parents ain't proud of you."
            )

    @start_daily_quotes.error
    async def start_daily_quotes_handler(self, ctx: Context, error: CommandError):
        if isinstance(error, MissingRole):
            await ctx.send("Failing like the weak you are, go find a gf or do some training.")

    @loop(hours=24, reconnect=True)
    async def daily_quote(self) -> None:
        quote = await _grab_quote()

        await self.bot.get_channel(899278487792279622).send(
            embed=create_embed(quotes_config(f"{quote['character']} - {quote['anime']}", quote["quote"]))
        )

    @daily_quote.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(QuotesCog(bot))
