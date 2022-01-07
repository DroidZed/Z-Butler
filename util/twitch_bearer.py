from httpx import AsyncClient

from config.main import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET


async def twitch_bearer() -> dict:

    """
    A Coroutine requesting a bearer token from Twitch API alongside other useful information.
    Returns:
        A dict containing the bearer, with an expiration date.
    """

    url = (
        f"https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}"
        f"&client_secret={TWITCH_CLIENT_SECRET}"
        f"&grant_type=client_credentials"
    )

    async with AsyncClient() as client:

        data = await client.post(url)

        return data.json()
