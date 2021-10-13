from spotify_client import SpotifyClient

from config.main import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID


class SpotiClient:

    _instance = None

    def __init__(self):

        self.client = SpotifyClient(SPOTIFY_CLIENT_ID,
                                    SPOTIFY_CLIENT_SECRET,
                                    identifier="Z-Bot-Singleton")

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

