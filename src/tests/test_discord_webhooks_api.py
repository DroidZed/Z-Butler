import pytest

from modules.networking import RequestError
from modules.networking import HttpAsyncClient


class TestDiscordWebHooksApi:
    @pytest.mark.asyncio
    async def test_sendingMessage(self):
        url = "https://discord.com/api/webhooks/1169582796877090846/qjyeBbeEQGE8dWOtXNgXQ5dkhoYHRXoD7OjJonkNDsC1sa_M87Y4ia24HWH5DlLPpNKg"

        result = await HttpAsyncClient().post(
            url, json={"content": "test test"}
        )

        print(result)

        assert not isinstance(result, RequestError)
