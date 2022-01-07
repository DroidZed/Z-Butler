# pylint: skip-file

from classes.singleton_class import SingletonClass
from util.twitch_bearer import twitch_bearer


class TwitchClient(metaclass=SingletonClass):

    """
    A wrapper Singleton around the twitch token, providing more
    tools for managing the state of the code like handling expiration date and expiring the token.
    """

    __slots__ = ["__data", "__token", "__expiration_day", "__is_token_expired"]

    def __init__(self, bearer: dict | None = None):

        self.__data = bearer
        self.__token = self.__data["access_token"]
        self.__expiration_day = (self.__data["expires_in"] // (60 * 60 * 24)) + 1
        self.__is_token_expired = False

    def __str__(self):
        return (
            f"Token:{self.__token}\n"
            f"Expires after: {self.__expiration_day} days.\n"
            f"Is the token expired: {self.__is_token_expired}."
        )

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
        self.__data = await twitch_bearer()

    def decrement_expiration(self):

        if self.__expiration_day > 0:
            self.__expiration_day -= 1
        else:
            self.is_token_expired = True
