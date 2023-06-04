from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ExternalUrls:
    spotify: str


@dataclass
class Artist:
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


@dataclass
class Image:
    height: int
    url: str
    width: int


@dataclass
class Album:
    album_type: str
    artists: List[Artist]
    available_markets: List[str]
    external_urls: ExternalUrls
    href: str
    id: str
    images: List[Image]
    name: str
    release_date: datetime
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str


@dataclass
class ExternalIDS:
    isrc: str


@dataclass
class Item:
    album: Album
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIDS
    external_urls: ExternalUrls
    href: str
    id: str
    is_local: bool
    name: str
    popularity: int
    preview_url: str
    track_number: int
    type: str
    uri: str


@dataclass
class Tracks:
    href: str
    items: List[Item]
    limit: int
    next: str
    offset: int
    previous: Optional[str]
    total: int
