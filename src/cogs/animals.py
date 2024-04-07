from discord import slash_command
from discord.ext.commands import (
    Bot,
    Cog,
)

from modules.animals_api import AnimalsAPI
from modules.animals_api import CatFact
from modules.views import CatPaws


class Animals(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()  # Create a slash command
    async def paw(self, ctx):
        async with ctx.typing():
            value = await AnimalsAPI().get_random_cat_facts()

        if not isinstance(value, CatFact):
            return await ctx.send(
                "Unable to pursue the request, the API failed."
            )
        await ctx.respond(
            f"{value.fact}", view=CatPaws()
        )  # Send a message with our View class that contains the button


def setup(bot: Bot):
    bot.add_cog(Animals(bot))
