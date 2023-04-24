import asyncio
import json

from modules.spotifyer.spotify_client import (
    SpotifyClient,
    authenticate_client,
)


async def main():

    auth = await authenticate_client()

    print(auth)

    c = SpotifyClient(auth)
    track = await c.search_song("Lost", "Linkin Park")
    print(json.dumps(track, sort_keys=True, indent=4))


asyncio.run(main())
