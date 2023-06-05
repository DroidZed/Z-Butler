from random import choice

from modules.networking import HttpAsyncClient
from utils import SingletonClass

from utils import Env


class TenorAPI(metaclass=SingletonClass):
    def __init__(
        self, http: HttpAsyncClient = HttpAsyncClient()
    ):
        self.client = http

    async def find_gif(self, topic: str):
        params = {
            "q": topic,
            "key": Env.TENOR_KEY,
            "limit": 101,
        }

        result = await self.client.get(
            url="https://g.tenor.com/v1/search",
            url_params=params,
        )

        if result.Data:
            link: str = choice(result.Data["results"])[
                "media"
            ][0]["gif"]["url"]
            return link

        else:
            return result.Error
