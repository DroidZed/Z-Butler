from discord import Button, ButtonStyle, Interaction
from discord.ui import View, button

from modules.views.feline_form import FelineForm


class CatPaws(View):
    @button(
        label="Touch me!", style=ButtonStyle.primary, emoji="🐾"
    )  # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button: Button, interaction: Interaction):
        # await interaction.response.send_message(
        #     "You touched the beans!", ephemeral=True
        # )  # Send a message when the button is clicked
        await interaction.response.send_modal(FelineForm(title="Purr"))
