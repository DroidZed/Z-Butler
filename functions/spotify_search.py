from spotify_client import SpotifyClient

from config.main import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


def spotify_search_rest(title: str, artist: str) -> dict:

    """
    Searches for a track using the spotify official REST API.
    Args:
        title: the title of the track
        artist: the name of the primary artist

    Returns:
        A dictionary containing the track's name, all artists who sang in, the album to which it belongs to
    and the link to the track on spotify (not to be confused with the api link).
    """

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
