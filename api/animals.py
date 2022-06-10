from httpx import AsyncClient


async def get_random_cat_facts() -> dict:
    return await __api_call("https://catfact.ninja/fact")


async def get_random_dog_picture() -> dict:
    return await __api_call("https://dog.ceo/api/breeds/image/random")


async def __api_call(url: str) -> dict:
    async with AsyncClient() as client:
        r = await client.get(url)

        return r.json()
