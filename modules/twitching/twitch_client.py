from typing import Any, Optional
from httpx import AsyncClient

from utils.singleton_class import SingletonClass
from config import Env


async def get_pfp(login: str) -> str | None:
    twitch_bearer_data = TwitchClient()

    # if I'm past the expiration date, refresh the token
    if twitch_bearer_data.is_token_expired:
        await twitch_bearer_data.refresh_token()

        return await get_pfp(login)

    headers = {
        "Authorization": f"Bearer {twitch_bearer_data.token}",
        "Client-Id": Env.TWITCH_CLIENT_ID,
    }

    url = f"https://api.twitch.tv/helix/search/channels?query={login}&live_only=true&first=2"

    async with AsyncClient(headers=headers) as client:
        query = await client.get(url)

        json = query.json()

        if not json["data"]:
            return

        return query.json()["data"][0]["thumbnail_url"]


async def authenticate() -> dict:
    params = {
        "client_id": Env.TWITCH_CLIENT_ID,
        "client_secret": Env.TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }

    async with AsyncClient() as client:
        data = await client.post(
            url="https://id.twitch.tv/oauth2/token",
            params=params,
        )

        return data.json()


class TwitchClient(metaclass=SingletonClass):
    """
    A wrapper Singleton around the twitch token, providing more
    tools for managing the state of the code like handling expiration date and expiring the token.
    """

    __slots__ = [
        "__data",
        "__token",
        "__expiration_day",
        "__is_token_expired",
    ]

    def __init__(
        self, data: Optional[dict[str, Any]] = None
    ):
        if data:
            self.__data = data
            self.__token = self.__data["access_token"]
            self.__expiration_day = (
                self.__data["expires_in"] // (60 * 60 * 24)
            ) + 1
            self.__is_token_expired = False

    def __str__(self):
        return (
            f"Token:{self.__token}\n"
            f"Expires after: {self.__expiration_day} days.\n"
            f"Is the token expired: {self.__is_token_expired}."
        )

    @property
    def token(self):
        return self.__token

    @property
    def expiration_day(self):
        return self.__expiration_day

    @property
    def is_token_expired(self):
        return self.__is_token_expired

    @token.setter
    def token(self, t):
        self.__token = t

    @expiration_day.setter
    def expiration_day(self, exp):
        self.__expiration_day = exp

    @is_token_expired.setter
    def is_token_expired(self, state):
        self.__is_token_expired = state

    async def refresh_token(self):
        self.__data = await authenticate()

    def decrement_expiration(self):
        if self.__expiration_day > 0:
            self.__expiration_day -= 1
        else:
            self.is_token_expired = True
