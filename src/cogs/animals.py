from discord import ApplicationContext, slash_command
from discord.ext.commands import Bot, Cog

from modules.animals_api import AnimalsAPI
from modules.animals_api import CatFact
from modules.views import CatPaws

# from modules.logging import LoggerHelper


class Animals(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @slash_command()  # Create a slash command
    async def paw(self, ctx: ApplicationContext) -> None:
        async with ctx.typing():
            value = await AnimalsAPI().get_random_cat_facts()

        if not isinstance(value, CatFact):
            await ctx.send("Unable to pursue the request, the API failed.")
            return
        await ctx.respond(
            f"{value.fact}", view=CatPaws()
        )  # Send a message with our View class that contains the button


def setup(bot: Bot) -> None:
    bot.add_cog(Animals(bot))
