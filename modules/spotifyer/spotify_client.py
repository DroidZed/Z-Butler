from httpx import AsyncClient
from modules.spotifyer.spoti_models import ClientAuth

from utils.singleton_class import SingletonClass
from config.main import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)

from functions.helpers import strToB64


async def authenticate_client() -> ClientAuth:

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f'Basic {strToB64(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}").decode()}',
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}

    async with AsyncClient() as clt:

        resp = await clt.post(
            url=url, data=data, headers=headers
        )

        json = resp.json()

        return ClientAuth(
            json["access_token"],
            json["token_type"],
            json["expires_in"],
        )


class SpotifyClient(metaclass=SingletonClass):
    def __init__(
        self, auth: ClientAuth | None = None
    ) -> None:

        if auth:
            self._token = auth.access_token
            self._expiry = auth.expires_in
            self._token_type = auth.token_type

    async def search_song(
        self, title: str, artist_name: str
    ):

        return await self.__search(
            f"artist: {artist_name} track: {title}",
            type=["track"],
            limit=1,
        )

    async def __search(
        self, query: str, type: list[str], limit: int
    ):

        headers = {
            "Authorization": f"{self._token_type} {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        params = {
            "q": query,
            "limit": limit,
            "type": " ".join(_ for _ in type),
        }

        url = "https://api.spotify.com/v1/search?"

        async with AsyncClient() as clt:

            resp = await clt.get(
                url=url, params=params, headers=headers
            )

            try:

                json = resp.json()

                return json

            except:
                return None
