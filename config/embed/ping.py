from util.colors import BOT_COLOR


def ping_config(pong: str) -> dict:
    return {
        "title": "Z Butler's Ping",
        "color": BOT_COLOR,
        "description": f"{pong}",
        "image": {"url": "https://c.tenor.com/ptYJsG8-K4MAAAAC/cats-ping-pong.gif"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
    }
