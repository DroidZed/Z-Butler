from modules.networking import HttpAsyncClient, RequestError

from utils import Env
from utils import strToB64, SingletonClass

from .melody_models import Album, Melody, Wave


class MelodyWave(metaclass=SingletonClass):
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
            "Authorization": f'Basic {strToB64(f"{Env.SPOTIFY_CLIENT_ID}:{Env.SPOTIFY_CLIENT_SECRET}").decode()}',
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"grant_type": "client_credentials"}

        resp = await self._client.post(
            url="https://accounts.spotify.com/api/token",
            body=data,
            headers=headers,
        )

        data = resp.Data

        if data:
            self._token = data["access_token"]
            self._token_type = data["token_type"]
            self._expiry = data["expires_in"]

            return self
        else:
            return resp.Error

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

        result = await self._client.get(
            url, headers, params
        )

        if result.Data:
            data = result.Data["tracks"]["items"][0]

            return Melody(
                track=data["name"],
                artists=[
                    art["name"] for art in data["artists"]
                ],
                album=Album(
                    name=data["album"]["name"],
                    art=data["album"]["images"][0],
                ),
                href=data["external_urls"]["spotify"],
            )
        else:
            return result.Error

    async def fetch_lyrics(
        self, title: str, artist: str | None = None
    ):
        res = await self._client.get(
            f"https://some-random-api.com/others/lyrics?title={title}{f' {artist}' if artist else ''}"
        )

        data = res.Data
        if data:
            return Wave(
                data["title"],
                data["author"],
                data["thumbnail"]["genius"],
                data["links"]["genius"],
                data["lyrics"],
                data["disclaimer"],
                data["source"]
            )
        else:
            return res.Error
