from modules.networking import HttpAsyncClient
from utils import SingletonClass
from .models import CatFact, DocPicture


class AnimalsAPI(metaclass=SingletonClass):
    def __init__(
        self, http: HttpAsyncClient = HttpAsyncClient()
    ):
        self.client = http

    async def get_random_cat_facts(self):
        result = await self.client.get(
            "https://catfact.ninja/fact"
        )

        if result.Data:
            data = result.Data

            return CatFact(
                fact=data["fact"], length=data["length"]
            )

        else:
            return result.Error

    async def get_random_dog_picture(self):
        result = await self.client.get(
            "https://dog.ceo/api/breeds/image/random"
        )

        if result.Data:
            data = result.Data

            return DocPicture(
                message=data["message"],
                status=data["status"],
            )

        else:
            return result.Error
