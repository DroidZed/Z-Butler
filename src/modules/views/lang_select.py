from discord import Button, ButtonStyle, Interaction
from discord.ui import View, button

from gtts import gTTS

CHOSEN_LANG = "./tts/chosen_lang.mp3"


class LangSelect(View):
    @button(label="Arabic", style=ButtonStyle.primary, emoji="🇸🇦")
    async def arabic_btn_callback(self, button: Button, interaction: Interaction):
        chosen_ar = gTTS(text="لقد اخترت اللغة العربية", lang="ar")
        chosen_ar.save(CHOSEN_LANG)

        await interaction.response.send_message("You selected arabic.")

    @button(label="English", style=ButtonStyle.primary, emoji="🇬🇧")
    async def eng_btn_callback(self, button: Button, interaction: Interaction):
        chosen_en = gTTS(text="You selected english", lang="en")
        chosen_en.save(CHOSEN_LANG)

        await interaction.response.send_message("You selected english.")
