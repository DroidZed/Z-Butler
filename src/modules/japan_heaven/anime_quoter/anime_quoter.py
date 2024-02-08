# from anime_api.apis import AnimechanAPI
from utils import SingletonClass
from modules.networking import HttpAsyncClient
from .quoter_models import AnimeQuote


class AnimeQuoter(metaclass=SingletonClass):
    def __init__(self) -> None:
        self.client = HttpAsyncClient()

    async def random_anime_quote(self):
        result = await self.client.get("https://animechan.xyz/api/random")

        if result.Error:
            return result.Error

        if result.Data:
            data = result.Data
            return AnimeQuote(
                anime=data["anime"],
                character=data["character"],
                quote=data["quote"],
            )
