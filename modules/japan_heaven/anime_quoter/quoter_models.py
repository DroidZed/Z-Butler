from dataclasses import dataclass


@dataclass(repr=True)
class AnimeQuote:
    anime: str
    character: str
    quote: str
