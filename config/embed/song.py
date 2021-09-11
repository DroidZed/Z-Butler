from config.main import COLOR


def song_config(**data) -> dict:
    return {
        "title": f"**{data['title']}**",
        "url": f"{data['song_url']}",
        "color": COLOR,
        "description": f"The song you've requested, by {data['artist']}",
        "image": {"url": f"{data['art_url']}"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail": {"url":
                          "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"},
        "footer": {
            "text": f"Songs by Genius Lyrics 💙",
            "icon_url": f"https://crypttv.com/wp-content/uploads/2020/10/59-598221_genius-lyrics-logo-transparent-clipart.png"}
    }
