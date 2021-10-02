from datetime import datetime

from config.colors import Colors


def playing_activity_config(name: str, mention: str, issuer: str, avatar_url: str, since: datetime = None) -> dict:
    return {
        "title": f"{name}",
        "description": f"{mention} has been `playing` ***{name}***{f' since {since}' if since else ''} 🎮",
        "color": Colors.BOT_COLOR,
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
