from httpx import AsyncClient

from classes.TwitchClient import TwitchClient
from config.main import TWITCH_CLIENT_ID


async def get_twitch_user_pfp(login: str) -> str | None:
    twitch_bearer_data = TwitchClient()

    # if I'm past the expiration date, refresh the token
    if twitch_bearer_data.is_token_expired:
        twitch_bearer_data.refresh_token()

        return

    else:
        headers = {
            "Authorization": f"Bearer {twitch_bearer_data.token}",
            "Client-Id": TWITCH_CLIENT_ID
        }

        url = f"https://api.twitch.tv/helix/search/channels?query={login}&live_only=true&first=2"

        async with AsyncClient(headers=headers) as client:
            x = await client.get(url)

            json = x.json()

            if not json["data"]:
                return

            return x.json()['data'][0]['thumbnail_url']
