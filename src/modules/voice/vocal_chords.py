import datetime

import pyttsx3


class VocalChords:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()

    def select_gender(self, gender: int) -> bool:
        if gender not in {0, 1}:
            return False

        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[gender].id)

        return True

    def create_mp3_from_text(self, msg: str, lang: str = "en") -> str:
        name = f"{datetime.datetime.now().timestamp}-tts.mp3"
        self.engine.save_to_file(msg, name)

        return name

        # tts.save(f"./tts/{name}")
