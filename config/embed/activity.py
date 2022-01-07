from datetime import datetime

from util.colors import BOT_COLOR


def activity_config(
    name: str,
    username: str,
    issuer: str,
    avatar_url: str,
    image_url: str,
    since: datetime = None,
) -> dict:
    config_dict = {
        "title": f"{username}'s Activity",
        "description": f"{name}{f' since {since}' if since else ''}",
        "color": BOT_COLOR,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {"text": f"Requested by {issuer} 💙", "icon_url": f"{avatar_url}"},
    }

    if image_url:
        config_dict["image"] = {"url": f"{image_url}"}

    return config_dict
