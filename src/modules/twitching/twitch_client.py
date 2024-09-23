from modules.networking import HttpAsyncClient

from utils import SingletonClass
from utils import Env
from .twitch_auth_client import TwitchAuthClient


class TwitchClient(metaclass=SingletonClass):
    """
    A wrapper Singleton around the twitch token, providing more
    tools for managing the state of the code like handling expiration date and expiring the token.
    """

    __slots__ = [
        "_auth_instance",
        "_client",
    ]

    def __init__(
        self,
        auth: TwitchAuthClient,
        http: HttpAsyncClient = HttpAsyncClient(),
    ):
        self._auth_instance = auth
        self._client = http

    async def get_pfp(self, login: str):
        # if I'm past the expiration date, refresh the token
        if self._auth_instance.is_token_expired:
            await self._auth_instance.refresh_token()

            return await self.get_pfp(login)

        headers = {
            "Authorization": f"Bearer {self._auth_instance.token}",
            "Client-Id": Env.TWITCH_CLIENT_ID,
        }

        query = await self._client.get(
            url=f"https://api.twitch.tv/helix/search/channels?query={login}&live_only=true&first=2",
            headers=headers,
        )

        return query.Data["data"][0]["thumbnail_url"] if query.Data else query.Error
