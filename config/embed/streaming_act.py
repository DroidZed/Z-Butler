from datetime import datetime

from config.colors import Colors


def streaming_activity_config(name: str,
                              since: datetime,
                              mention: str,
                              issuer: str,
                              avatar_url: str,
                              platform: str,
                              stream_url: str = None,
                              streamed_game: str = None) -> dict:

    dic = {
        "title": f"{name}",
        "description": f"{mention} has been `streaming` ***this*** since {since} 👻",
        "color":  __change_platform_color(platform),
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "icon_url": f"{avatar_url}"
        }
    }

    if stream_url:
        dic["description"] += f"\nFollow this [link]({stream_url}) to catch them **live** 🔴 on `{platform}` !"

    if streamed_game:
        dic["description"] = dic["description"].replace(
            "this", f"{streamed_game}")

    return dic


def __change_platform_color(platform: str):
    if platform == 'Twitch':
        return Colors.TWITCH_PURPLE
    elif platform == 'YouTube':
        return Colors.YOUTUBE_RED
    else:
        return Colors.BOT_COLOR