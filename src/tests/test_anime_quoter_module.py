from json import dumps

import pytest

from modules.japan_heaven.anime_quoter import AnimeQuoter


class TestAnimeQuoterModule:
    @pytest.mark.asyncio
    async def test_should_provide_a_random_quote(self):
        res = await AnimeQuoter().random_anime_quote()

        assert res is not None

        print(dumps(res.serialize(), indent=4))
