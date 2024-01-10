import pytest

from modules.networking import RequestError
from modules.tenor_api import TenorAPI


class TestTenorAPI:
    @pytest.mark.asyncio
    async def test_should_return_valid_result(self):
        result = await TenorAPI().find_gif("cats")

        assert not isinstance(result, RequestError)

        print(result)
