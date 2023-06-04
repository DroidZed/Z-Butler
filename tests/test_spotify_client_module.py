import pytest

from json import dumps
from typing import Optional

from modules.spotify_helper import SpotifyClient


class TestSpotifyClientModule:
    _client = SpotifyClient()

    @pytest.mark.asyncio
    async def test_should_provide_a_connected_instance(
        self,
    ):
        res = await self._client.authenticate_client()

        assert res != None

        self._client = res

    @pytest.mark.asyncio
    async def test_should_consume_a_valid_song_data(
        self,
    ):
        track = await self._client.search_song(
            title="MOTTO", artist="NF"
        )

        assert track != None
