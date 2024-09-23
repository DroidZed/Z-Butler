import asyncio
import os

from discord import FFmpegPCMAudio, Forbidden, HTTPException, Member, VoiceState
from discord.ext.commands import (
    Bot,
    Cog,
)
from gtts import gTTS
from modules.embedder.embedder_machine import generate_embed
from modules.views import LangSelect

WELCOME_MSG = "./tts/welcome_message.mp3"
OPEN_DM = "./tts/open_dm.mp3"
LANG_SELECT_REQ = "./tts/lang_select_req.mp3"
CHOSEN_LANG = "chosen_lang.mp3"


class Verification(
    Cog,
    name="Verification",
    description="Admin commands for verification",
):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if (
            member != self.bot.user
            and after.channel
            and after.channel.id == 1122519447186440226
        ):
            await asyncio.sleep(1)
            vc = await after.channel.connect()

            open_dms_msg = gTTS(text="Open your dms", lang="en")
            open_dms_msg.save(OPEN_DM)

            pls_select_lang = gTTS(text="Please select a language", lang="en")
            pls_select_lang.save(LANG_SELECT_REQ)

            welcome_msg = gTTS(
                text="Hello, welcome to the server! To proceed with the verification, kindly allow us to send you DMs. The verification process will start shortly after you've opened your DMs. Thank you.",
                lang="en",
            )
            welcome_msg.save(WELCOME_MSG)

            while not await self.can_dm_user(member):
                vc.play(FFmpegPCMAudio(OPEN_DM))
                while vc.is_playing():
                    await asyncio.sleep(1)
            else:
                vc.play(FFmpegPCMAudio(WELCOME_MSG))
                while vc.is_playing():
                    await asyncio.sleep(1)

                embed = generate_embed(
                    "Verification",
                    description="Choose your preferred language",
                )

                await member.send(embed=embed, view=LangSelect())

                dirname = os.path.dirname(__file__)

                file = os.path.join(dirname, f"../../tts/{CHOSEN_LANG}")

                while not os.path.isfile(file):
                    vc.play(FFmpegPCMAudio(LANG_SELECT_REQ))
                    while vc.is_playing():
                        await asyncio.sleep(1)

                    await asyncio.sleep(3)
                else:
                    vc.play(FFmpegPCMAudio(f"./tts/{CHOSEN_LANG}"))
                    while vc.is_playing():
                        await asyncio.sleep(1)

                    os.remove(WELCOME_MSG)
                    os.remove(OPEN_DM)
                    os.remove(LANG_SELECT_REQ)
                    os.remove(f"./tts/{CHOSEN_LANG}")

                    await vc.disconnect()

    async def can_dm_user(self, user: Member) -> bool:
        try:
            await user.send()
            return True
        except Forbidden:
            return False
        except HTTPException:
            return True


def setup(bot: Bot) -> None:
    bot.add_cog(Verification(bot))
