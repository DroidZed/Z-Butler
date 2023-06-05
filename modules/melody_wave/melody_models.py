from dataclasses import dataclass
from typing import List


@dataclass
class Album:
    name: str
    art: str


@dataclass
class Melody:
    track: str
    artists: List[str]
    album: Album
    href: str


@dataclass
class Wave:
    title: str
    artist: str
    art_url: str
    song_url: str
    lyrics: str
