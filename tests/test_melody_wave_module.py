import pytest

from modules.melody_wave import MelodyWave


class TestMelodyWaveModule:
    _client = MelodyWave()

    @pytest.mark.asyncio
    async def test_should_provide_a_connected_instance(
        self,
    ):
        res = await self._client.authenticate_client()

        assert isinstance(res, MelodyWave)

        self._client = res

        print(self._client._token)

    @pytest.mark.asyncio
    async def test_should_consume_a_valid_song_data(
        self,
    ):
        track = await self._client.search_song(
            title="MOTTO", artist="NF"
        )

        assert track != None
