from discord import InputTextStyle, Interaction
from discord.ui import Modal, InputText

from modules.embedder import EmbedderMachine, Zembed, ZembedField


class FelineForm(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label="What's your name?"))
        self.add_item(
            InputText(
                label="What do you like about cats?", style=InputTextStyle.long
            )
        )

    async def callback(self, interaction: Interaction):
        machine = EmbedderMachine()
        machine.set_embed_components("Survey Results, meow 😸")
        machine.add_fields(
            *[
                ZembedField(
                    name=self.children[0].label, value=self.children[0].value
                ),
                ZembedField(
                    name=self.children[1].label, value=self.children[1].value
                ),
            ]
        )
        await interaction.response.send_message(embeds=[machine.embed])
