from coinpaprika_async import MiscelanousEndpoints
from utils import SingletonClass


class CoinManager(metaclass=SingletonClass):
    def __init__(self, endpoint=MiscelanousEndpoints()):
        self.endpoint = endpoint

    async def convert_coin(
        self, base: str, target: str, amount: int
    ):
        return await self.endpoint.price_converter(
            base_currency_id=base,
            quote_currency_id=target,
            amount=amount,
        )

    # async def search_coin(self, code: str):
    #     return await self.endpoint.search()
