from modules.http.http_async_client import HttpAsyncClient

from utils.singleton_class import SingletonClass
from config.main import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)
from utils.helpers import strToB64


class SpotifyClient(metaclass=SingletonClass):
    def __init__(
        self,
        http: HttpAsyncClient = HttpAsyncClient(),
    ) -> None:
        try:
            self._token = ""
            self._token_type = ""
            self._expiry = 0
            self._client = http
        except:
            return

    async def search_song(self, title: str, artist: str):
        return await self.__search(
            query=title,
            artist=artist,
            type=["track"],
            limit=1,
        )

    async def authenticate_client(self):
        headers = {
            "Authorization": f'Basic {strToB64(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}").decode()}',
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"grant_type": "client_credentials"}

        resp = await self._client.post(
            url="https://accounts.spotify.com/api/token",
            body=data,
            headers=headers,
        )

        if resp and isinstance(resp, dict):
            self._token = resp["access_token"]
            self._token_type = resp["token_type"]
            self._expiry = resp["expires_in"]

            return self
        else:
            return

    async def __search(
        self,
        query: str,
        artist: str,
        type: list[str],
        limit: int,
    ):
        headers = {
            "Authorization": f"{self._token_type} {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        params = {
            "q": f"{query} aritst:{artist}",
            "limit": limit,
            "type": " ".join(_ for _ in type),
        }

        url = "https://api.spotify.com/v1/search"

        return await self._client.get(url, headers, params)
