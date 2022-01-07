from httpx import AsyncClient


async def currency_exchange(base: str, target: str) -> dict:
    url = f"https://api.cryptonator.com/api/ticker/{base.lower()}-{target.lower()}"

    async with AsyncClient() as client:
        res = await client.get(url=url)

        return res.json()
