from datetime import datetime


class ExternalUrls:
    def __init__(self, spotify: str) -> None:
        self.spotify = spotify


class Artist:
    def __init__(
        self,
        external_urls: ExternalUrls,
        href: str,
        id: str,
        name: str,
        type: str,
        uri: str,
    ) -> None:
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.name = name
        self.type = type
        self.uri = uri


class Image:
    def __init__(
        self, height: int, url: str, width: int
    ) -> None:
        self.height = height
        self.url = url
        self.width = width


class Album:
    def __init__(
        self,
        album_type: str,
        artists: list[Artist],
        available_markets: list[str],
        external_urls: ExternalUrls,
        href: str,
        id: str,
        images: list[Image],
        name: str,
        release_date: datetime,
        release_date_precision: str,
        total_tracks: int,
        type: str,
        uri: str,
    ) -> None:
        self.album_type = album_type
        self.artists = artists
        self.available_markets = available_markets
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.total_tracks = total_tracks
        self.type = type
        self.uri = uri


class ExternalIDS:
    def __init__(self, isrc: str) -> None:
        self.isrc = isrc


class Item:
    def __init__(
        self,
        album: Album,
        artists: list[Artist],
        available_markets: list[str],
        disc_number: int,
        duration_ms: int,
        explicit: bool,
        external_ids: ExternalIDS,
        external_urls: ExternalUrls,
        href: str,
        id: str,
        is_local: bool,
        name: str,
        popularity: int,
        preview_url: str,
        track_number: int,
        type: str,
        uri: str,
    ) -> None:
        self.album = album
        self.artists = artists
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_ids = external_ids
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.is_local = is_local
        self.name = name
        self.popularity = popularity
        self.preview_url = preview_url
        self.track_number = track_number
        self.type = type
        self.uri = uri


class Tracks:
    def __init__(
        self,
        href: str,
        items: list[Item],
        limit: int,
        next: str,
        offset: int,
        previous: None,
        total: int,
    ) -> None:
        self.href = href
        self.items = items
        self.limit = limit
        self.next = next
        self.offset = offset
        self.previous = previous
        self.total = total


class ClientAuth:
    def __init__(
        self,
        access_token: str,
        token_type: str,
        expires_in: int,
    ) -> None:
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
