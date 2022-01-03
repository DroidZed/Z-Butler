from classes.SingletonClass import SingletonClass
from util.twitch_bearer import twitch_bearer


class TwitchClient(metaclass=SingletonClass):

    """
    A class to interact with the twitch API. Gives an object containing the token, alongside others
    user data.
    """

    __slots__ = ["_data", "_token", "_expiration_day", "_is_token_expired"]

    def __init__(self, bearer: dict | None = None):

        self._data = bearer
        self._token = self._data["access_token"]
        self._expiration_day = (self._data["expires_in"] // (60 * 60 * 24)) + 1
        self._is_token_expired = False

    def __str__(self):
        return f"Token:{self._token}\n" \
               f"Expires after: {self._expiration_day} days.\n" \
               f"Is the token expired: {self._is_token_expired}."

    @property
    def token(self):
        return self._token

    @property
    def expiration_day(self):
        return self._expiration_day

    @property
    def is_token_expired(self):
        return self._is_token_expired

    @token.setter
    def token(self, t):
        self._token = t

    @expiration_day.setter
    def expiration_day(self, exp):
        self._expiration_day = exp

    @is_token_expired.setter
    def is_token_expired(self, state):
        self._is_token_expired = state

    async def refresh_token(self):
        self._data = await twitch_bearer()

    def decrement_expiration(self):

        if self._expiration_day > 0:
            self._expiration_day -= 1
        else:
            self.is_token_expired = True
