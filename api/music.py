from httpx import AsyncClient
from spotify_client import SpotifyClient

from config.main import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


def find_song(title: str, artist: str) -> dict:
    client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, identifier="Z-Bot-Singleton")
    res = client.search(f"{title} {artist}", search_types=["track"], limit=1)

    data = res["tracks"]["items"][0]

    return {
        "track": data["name"],
        "artists": [art["name"] for art in data["artists"]],
        "album": {
            "name": data["album"]["name"],
            "art": data["album"]["images"][0],
        },
        "href": data["external_urls"]["spotify"],
    }


async def fetch_lyrics(title: str, artist: str | None = None) -> dict:
    artist = artist.replace(" ", "%20") if artist else None

    title = title.replace(" ", "%20")

    async with AsyncClient() as client:
        res = await client.get(f"https://some-random-api.ml/lyrics?title={title}{'%20' + artist if artist else ''}")

        data = res.json()

    if "error" in data:
        return {
            "valid": False,
        }

    return {
        "title": data["title"],
        "artist": data["author"],
        "art_url": data["thumbnail"]["genius"],
        "song_url": data["links"]["genius"],
        "lyrics": data["lyrics"],
        "valid": True,
    }
