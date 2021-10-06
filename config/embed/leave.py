from util.colors import BOT_COLOR


def leave_config(username: str, member_id: int) -> dict:
    return {
        "title": f"{username} Left us.",
        "color": BOT_COLOR,
        "description": f"<@{member_id}> "
                       "got sucked into a black hole <a:black_hole:796434656605765632>, long forgotten.",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"},
        "footer": {
            "text": f"We shall never remember those who left our cause.",
            "icon_url": f"https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"}
    }
