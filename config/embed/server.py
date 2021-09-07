from config.main import COLOR


def server_stats_config(title: str):

    return {
        "color": COLOR,
        "thumbnail": {
            "url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "author": {
            "name": f"{title}",
            "icon_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        },
        "footer": {
            "text": f"From the best bot ever, in the best server ever 💙",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        }
    }
