from typing import Optional

from modules.networking import HttpAsyncClient
from utils.singleton_class import SingletonClass


class HaikuAPI(metaclass=SingletonClass):
    async def getHaiku(self, topic: str) -> Optional[str]:
        client = HttpAsyncClient()

        res = await client.get(
            "https://www.freshbots.org/api/poem",
            url_params={"topic": topic, "style": "haiku"},
        )

        return res.Data if res.Data else None
