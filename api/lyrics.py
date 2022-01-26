from httpx import AsyncClient


async def lyrics(title: str, artist: str = None) -> dict:

    artist = artist.replace(" ", "%20")

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
