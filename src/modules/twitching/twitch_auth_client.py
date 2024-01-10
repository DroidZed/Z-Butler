from utils import Env
from modules.networking import HttpAsyncClient


class TwitchAuthClient:
    def __init__(
        self, http: HttpAsyncClient = HttpAsyncClient()
    ):
        self._client = http
        self.__token = ""
        self.__expiration_day = 0
        self.__is_token_expired = False

    @property
    def token(self):
        return self.__token

    @property
    def expiration_day(self):
        return self.__expiration_day

    @property
    def is_token_expired(self):
        return self.__is_token_expired

    @token.setter
    def token(self, t):
        self.__token = t

    @expiration_day.setter
    def expiration_day(self, exp):
        self.__expiration_day = exp

    @is_token_expired.setter
    def is_token_expired(self, state):
        self.__is_token_expired = state

    async def refresh_token(self):
        await self.authenticate()

    def decrement_expiration(self):
        if self.__expiration_day > 0:
            self.__expiration_day -= 1
        else:
            self.is_token_expired = True

    async def authenticate(self):
        result = await self._client.post(
            url="https://id.twitch.tv/oauth2/token",
            url_params={
                "client_id": Env.TWITCH_CLIENT_ID,
                "client_secret": Env.TWITCH_CLIENT_SECRET,
                "grant_type": "client_credentials",
            },
        )

        if result.Data:
            self.__expiration_day = (
                result.Data["expires_in"] // (60 * 60 * 24)
            ) + 1
            self.__token = result.Data["access_token"]
