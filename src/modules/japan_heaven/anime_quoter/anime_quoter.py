from anime_api.apis import AnimechanAPI
from utils import SingletonClass
from modules.networking import HttpAsyncClient
from .models import AnimeQuote


class AnimeQuoter(metaclass=SingletonClass):
    def __init__(self) -> None:
        self.client = HttpAsyncClient()

    async def random_anime_quote(self):
        result = await self.client.get("https://animechan.xyz/api/random")

        if result.Error:
            raise result.Error

        return AnimeQuote(
            anime=result.Data["anime"],
            character=result.Data["character"],
            quote=result.Data["quote"],
        )
