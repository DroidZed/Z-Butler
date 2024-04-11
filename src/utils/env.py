from decouple import config
from dataclasses import dataclass


@dataclass
class Env:
    # Get tokens and keys from env.
    TOKEN = config("API_TOKEN")
    TENOR_KEY = config("TENOR_API_KEY")
    RAPID_API_KEY = config("RAPID_API_KEY")

    # Spotify credentials
    SPOTIFY_CLIENT_SECRET = config("SPOTIPY_CLIENT_SECRET")
    SPOTIFY_CLIENT_ID = config("SPOTIPY_CLIENT_ID")

    # Twitch credentials
    TWITCH_CLIENT_ID = config("TWITCH_CLIENT_ID")
    TWITCH_CLIENT_SECRET = config("TWITCH_CLIENT_SECRET")

    # Twitter credentials
    TWITTER_API_KEY = config("TWITTER_API_KEY")
    TWITTER_SECRET_KEY = config("TWITTER_SECRET_KEY")
    TWITTER_OAUTH2_CLIENT_ID = config("TWITTER_OAUTH2_CLIENT_ID")
    TWITTER_OAUTH2_CLIENT_SECRET = config("TWITTER_OAUTH2_CLIENT_SECRET")

    # Default bot config
    PREFIX: str = "Z"
    OWNER_ID = 443064096124960779
    GUILD_ID = 1005448304374583386
    CROWN_ROLE_ID = 1005544779473489981
    BOT_ID = 759844892443672586
    SERVER_IMAGE = "https://cdn.discordapp.com/attachments/1012475750940672080/1071067387144712202/7ccc95853e9c7c2b09930d55b1d795aa.png"

    # MongoDB Config
    MDB_SRV = config("MDB_SRV")
    DB_NAME = config("DB_NAME")

    # Colors
    BOT_COLOR = 0x0027B3
    SPOTIFY_COLOR = 0x1DB954
    VIP_COLOR = 0xFFBD02
    CROWN_COLOR = 0x7109A1
    YOUTUBE_RED = 0xFF0000
    TWITCH_PURPLE = 0x9146FF
    TWITTER_COLOR = 0x1DA1F2
