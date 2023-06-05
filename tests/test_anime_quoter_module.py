import pytest
from json import dumps

from modules.japan_heaven.anime_quoter import AnimeQuoter


class TestAnimeQuoterModule:
    api = AnimeQuoter()

    @pytest.mark.asyncio
    async def test_shoud_provide_a_random_quote(self):
        res = await self.api.random_anime_quote()

        print(dumps(res, indent=4))

        assert res is not None
