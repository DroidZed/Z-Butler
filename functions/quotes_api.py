from httpx import AsyncClient


async def anime_quotes() -> dict:

    async with AsyncClient() as client:
        query = await client.get("https://animechan.vercel.app/api/random")

        return query.json()
