from util.twitch_bearer import twitch_bearer


class TwitchClient:

    _instance = None

    __slots__ = ["_data", "_token", "_expiration_day", "_is_token_expired"]

    def __init__(self):

        self._data = twitch_bearer()
        self._token = self._data["access_token"]
        self._expiration_day = (self._data["expires_in"] // (60 * 60 * 24)) + 1
        self._is_token_expired = False

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __repr__(self):
        return f"Token:{self._token}" \
               f"\nExpiration day: {self._expiration_day}" \
               f"\nIs the token expired: {self._is_token_expired}"

    def __str__(self):
        return f"Token:{self._token}" \
               f"\nExpiration day: {self._expiration_day}" \
               f"\nIs the token expired: {self._is_token_expired}"

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

    def refresh_token(self):
        self._data = twitch_bearer()

    def increment_expiration(self):
        self._expiration_day += 1

    def decrement_expiration(self):

        if self._expiration_day > 0:
            self._expiration_day -= 1

        if self._expiration_day <= 0:
            self.is_token_expired = True
