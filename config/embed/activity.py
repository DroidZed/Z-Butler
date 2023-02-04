from datetime import datetime

from config.colors import TWITCH_PURPLE, BOT_COLOR, YOUTUBE_RED, SPOTIFY_COLOR
from config.links import server_image


def spotify_config(mention: str, song: str, album: str, artist: str, art: str, link: str) -> dict:
    return {
        "title": f"**{song}**",
        "color": SPOTIFY_COLOR,
        "description": f"{mention} is listening to this song by _{artist}_\nFrom the album **{album}**."
        f"\n Check it out -> [link]({link})",
        "image": {"url": f"{art}"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "footer": {
            "text": "Songs params provided by Spotify 💚",
            "icon_url": "https://1000logos.net/wp-content/uploads/2017/08/Spotify-Logo.png",
        },
    }


def streaming_activity_config(
    name: str,
    mention: str,
    issuer: str,
    avatar_url: str,
    platform: str,
    streamer_pfp: str | None = None,
    stream_url: str | None = None,
    streamed_game: str | None = None,
) -> dict:
    dic = {
        "title": f"{name}",
        "description": f"{mention} is `streaming` ***this*** 👻",
        "color": __change_platform_color(platform),
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "url": f"{stream_url}",
        "footer": {"text": f"Requested by {issuer} 💙", "icon_url": f"{avatar_url}"},
    }

    if stream_url:
        dic["description"] += f"\nFollow this [link]({stream_url}) to catch them **LIVE** 🔴 on `{platform}` !"

    if streamed_game:
        dic["description"] = dic["description"].replace("this", f"{streamed_game}")

    if streamer_pfp:
        dic["image"] = {"url": f"{streamer_pfp}"}

    return dic


def __change_platform_color(platform: str) -> int:
    match platform:

        case "Twitch":
            return TWITCH_PURPLE
        case "YouTube":
            return YOUTUBE_RED
        case _:
            return BOT_COLOR


def playing_activity_config(
    name: str, mention: str, issuer: str, avatar_url: str, since: datetime | None = None
) -> dict:
    return {
        "title": f"{name}",
        "description": f"{mention} has been `playing` ***{name}***{f' since {since}' if since else ''} 🎮",
        "color": BOT_COLOR,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "footer": {"text": f"Requested by {issuer} 💙", "icon_url": f"{avatar_url}"},
    }


def activity_config(
    name: str,
    username: str,
    issuer: str,
    avatar_url: str,
    image_url: str | None = None,
    since: datetime | None = None,
) -> dict:
    config_dict = {
        "title": f"{username}'s Activity",
        "description": f"{name}{f' since {since}' if since else ''}",
        "color": BOT_COLOR,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "footer": {"text": f"Requested by {issuer} 💙", "icon_url": f"{avatar_url}"},
    }

    if image_url:
        config_dict["image"] = {"url": f"{image_url}"}

    return config_dict
