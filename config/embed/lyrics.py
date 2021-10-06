from util.colors import BOT_COLOR


def lyrics_config(**data) -> dict:
    return {
        "title": f"**{data['title']}** by {data['artist']}",
        "url": data['song_url'],
        "color": BOT_COLOR,
        "description": data['lyrics'],
        "image": {"url": f"{data['art_url']}"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        },
        "thumbnail": {
            "url":
                "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": f"Lyrics by Genius Lyrics 💙",
            "icon_url":
                f"https://crypttv.com/wp-content/uploads/2020/10/59-598221_genius-lyrics-logo-transparent-clipart.png"
        }
    }
