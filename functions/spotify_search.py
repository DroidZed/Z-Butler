from classes.SpotiClient import SpotiClient


def spotify_search_rest(title: str, artist: str) -> dict:

    res = SpotiClient().client.search(
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
