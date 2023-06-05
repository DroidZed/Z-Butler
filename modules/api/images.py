from random import choice

from httpx import AsyncClient

from config import Env


async def find_gif(topic: str) -> dict:
    params = {"q": topic, "key": Env.TENOR_KEY, "limit": 101}

    async with AsyncClient() as client:
        result = await client.post(url="https://g.tenor.com/v1/search", params=params)

        data = result.json()

        return choice(data["results"])
