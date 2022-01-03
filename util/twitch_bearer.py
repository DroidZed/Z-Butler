from httpx import AsyncClient

from config.main import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET


async def twitch_bearer() -> dict:

    url = f"https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_CLIENT_SECRET}" \
          f"&grant_type=client_credentials"

    async with AsyncClient() as client:

        data = await client.post(url)

        return data.json()
