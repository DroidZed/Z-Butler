from spotify_client import SpotifyClient

from config.main import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


def spotify_search_rest(title: str, artist: str) -> dict:

    client = SpotifyClient(SPOTIFY_CLIENT_ID,
                           SPOTIFY_CLIENT_SECRET,
                           identifier="Z-Bot-Singleton")

    res = client.search(
        f"{title} {artist}",
        search_types=["track"],
        limit=1)

    data = res["tracks"]["items"][0]

    return {
        "track": data["name"],
        "artists": [art["name"] for art in data["artists"]],
        "album": {
            "name": data["album"]["name"],
            "art": data["album"]["images"][0],
        },
        "href": data['external_urls']['spotify']
    }
