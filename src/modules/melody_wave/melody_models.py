from dataclasses import dataclass
from typing import List


@dataclass(repr=True)
class Album:
    name: str
    art: str


@dataclass(repr=True)
class Melody:
    track: str
    artists: List[str]
    album: Album
    href: str


@dataclass(repr=True)
class Wave:
    title: str
    artist: str
    art_url: str
    song_url: str
    lyrics: str
    disclaimer: str
    source: int
