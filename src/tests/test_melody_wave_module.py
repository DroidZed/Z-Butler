import pytest
from modules.melody_wave import Melody, MelodyWave, Wave


class TestMelodyWaveModule:
    _client = MelodyWave()

    @pytest.mark.asyncio
    async def test_should_provide_a_connected_instance(
        self,
    ):
        res = await self._client.authenticate_client()

        assert isinstance(res, MelodyWave)

        self._client = res

    @pytest.mark.asyncio
    async def test_should_consume_a_valid_song_data(
        self,
    ):
        result = await self._client.search_song(title="HOPE", artist="NF")

        assert result is not None

        assert isinstance(result, Melody)

    @pytest.mark.asyncio
    async def test_should_fetch_lyrics(self):
        lyrics = await self._client.fetch_lyrics("HOPE", "NF")

        assert lyrics is not None

        assert isinstance(lyrics, Wave)
