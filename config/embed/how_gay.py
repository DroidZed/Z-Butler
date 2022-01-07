from util.colors import BOT_COLOR


def how_gay_config(username: str, mention: str, rate: int, msg: str) -> dict:
    return {
        "title": f"{username}'s Gay Level",
        "color": BOT_COLOR,
        "description": f"**{mention} is {rate}% gay** 🏳️‍🌈\n{msg}",
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
    }
