import pytest

from modules.networking import HttpAsyncDownloader


class TestHttpDownloader:
    @pytest.mark.asyncio
    async def test_should_download_file(self):
        client = HttpAsyncDownloader()
        await client.get_file_from_url(
            "https://api.coinpaprika.com/v1/coins",
            "./db.json",
        )

        with open("./db.json", "r") as f:
            assert f is not None
