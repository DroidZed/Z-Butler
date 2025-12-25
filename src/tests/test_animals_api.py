import pytest

from modules.animals_api import (
    AnimalsAPI,
    CatFact,
    DocPicture,
)


class TestAnimalsAPI:
    @pytest.mark.asyncio
    async def test_should_give_valid_cat_fact(self):
        cat_fact = await AnimalsAPI().get_random_cat_facts()

        assert isinstance(cat_fact, CatFact)

        print(cat_fact)

    @pytest.mark.asyncio
    async def test_should_fetch_dog_picture_successfully(
        self,
    ):
        dog_pic = await AnimalsAPI().get_random_dog_picture()

        assert isinstance(dog_pic, DocPicture)

        print(dog_pic)
