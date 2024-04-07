import pytest

from modules.haiku import HaikuAPI


class TestHaikuApi:

    @pytest.mark.asyncio
    async def test_should_return_me_a_random_python_haiku(self):

        result = await HaikuAPI().getHaiku("python")

        assert result != None

        print(result)
