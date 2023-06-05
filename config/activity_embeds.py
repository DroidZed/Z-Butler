from datetime import datetime
from typing import Optional

from config import Env


def spotify_config(
    mention: str,
    song: str,
    album: str,
    artist: str,
    art: str,
    link: str,
):
    return {
        "title": f"**{song}**",
        "color": Env.SPOTIFY_COLOR,
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
    streamer_pfp: Optional[str] = None,
    stream_url: Optional[str] = None,
    streamed_game: Optional[str] = None,
):
    def change_platform_color(platform: str):
        match platform:
            case "Twitch":
                return Env.TWITCH_PURPLE
            case "YouTube":
                return Env.YOUTUBE_RED
            case _:
                return Env.BOT_COLOR

    def resolve_desc(
        stream_url: Optional[str],
        streamed_game: Optional[str],
        desc: str,
    ):
        if stream_url:
            desc += f"\nFollow this [link]({stream_url}) to catch them **LIVE** 🔴 on `{platform}` !"

        if streamed_game:
            desc = desc.replace("this", f"{streamed_game}")

        return desc

    dic = {
        "title": f"{name}",
        "description": resolve_desc(
            stream_url,
            streamed_game,
            f"{mention} is `streaming` ***this*** 👻",
        ),
        "color": change_platform_color(platform),
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "url": f"{stream_url}",
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "icon_url": f"{avatar_url}",
        },
    }

    if streamer_pfp:
        dic["image"] = {"url": f"{streamer_pfp}"}

    return dic


def playing_activity_config(
    name: str,
    mention: str,
    issuer: str,
    avatar_url: str,
    since: Optional[datetime] = None,
):
    return {
        "title": f"{name}",
        "description": f"{mention} has been `playing` ***{name}***{f' since {since}' if since else ''} 🎮",
        "color": Env.BOT_COLOR,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "icon_url": f"{avatar_url}",
        },
    }


def activity_config(
    name: str,
    username: str,
    issuer: str,
    avatar_url: str,
    image_url: Optional[str] = None,
    since: Optional[datetime] = None,
):
    def resolve_image_url(image_url: Optional[str]):
        return (
            image_url
            if image_url
            else "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        )

    config_dict = {
        "title": f"{username}'s Activity",
        "description": f"{name}{f' since {since}' if since else ''}",
        "image": {"url": resolve_image_url(image_url)},
        "color": Env.BOT_COLOR,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "icon_url": f"{avatar_url}",
        },
    }

    return config_dict
