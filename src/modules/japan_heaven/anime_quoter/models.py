from dataclasses import dataclass

from utils import Model


@dataclass()
class AnimeQuote(Model):
    anime: str
    character: str
    quote: str

    def serialize(self):
        return {
            "anime": self.anime,
            "character": self.character,
            "quote": self.quote,
        }
