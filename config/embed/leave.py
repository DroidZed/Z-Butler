from config.main import COLOR


def leave_config(username: str, id: int) -> dict:
    return {
        "title": f"{username} Left us.",
        "color": COLOR,
        "description": f"<@{id}> got sucked into a blackhole <a:black_hole:796434656605765632>, long forgotten.",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "footer": {
            "text": f"We shall never remember those who left our cause.",
            "url": f"https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"}
    }
