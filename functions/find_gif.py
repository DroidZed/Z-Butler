from random import choice

from config.main import TENOR_KEY
from httpx import AsyncClient


async def find_gif(topic: str) -> dict:

    url = "https://g.tenor.com/v1/search"

    params = {
        'q': topic,
        'key': TENOR_KEY,
        'limit': 1
    }

    async with AsyncClient() as client:
        r = await client.post(url=url, params=params)

        data = r.json()

        return choice(data['results'])
