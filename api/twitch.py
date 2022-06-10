from httpx import AsyncClient

from classes.twitch_client import TwitchClient
from config.main import TWITCH_CLIENT_ID


async def get_pfp(login: str) -> str | None:
    twitch_bearer_data = TwitchClient()

    # if I'm past the expiration date, refresh the token
    if twitch_bearer_data.is_token_expired:
        await twitch_bearer_data.refresh_token()

        return get_pfp(login)

    headers = {
        "Authorization": f"Bearer {twitch_bearer_data.token}",
        "Client-Id": TWITCH_CLIENT_ID,
    }

    url = f"https://api.twitch.tv/helix/search/channels?query={login}&live_only=true&first=2"

    async with AsyncClient(headers=headers) as client:
        query = await client.get(url)

        json = query.json()

        if not json["params"]:
            return

        return query.json()["params"][0]["thumbnail_url"]
