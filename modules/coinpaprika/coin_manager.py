from coinpaprika_async import Client as CoinpaprikaClient
from utils import SingletonClass


class CoinManager(metaclass=SingletonClass):
    def __init__(
        self,
        coinpaprika_client: CoinpaprikaClient = CoinpaprikaClient(),
    ):
        self.client = coinpaprika_client

    async def convert_coin(
        self, base: str, target: str, amount: float
    ):
        return await self.client.price_converter(
            {
                "base_currency_id": base,
                "quote_currency_id": target,
                "amount": amount,
            }
        )
