from httpx import AsyncClient


async def quotes() -> dict:
    async with AsyncClient() as client:
        query = await client.get("https://animechan.vercel.app/api/random")

        return query.json()
