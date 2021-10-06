from util.colors import BOT_COLOR


def user_stats(username: str, tag: str, avatar_url: str) -> dict:
    return {
        "title": f"**{username}**'s Stats",
        "description": f"{tag}'s information.",
        "color": BOT_COLOR,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {"url": avatar_url},
        "footer": {
            "text": 'Delivered by your trusty bot, Z Butler 💙',
            'icon_url': 'https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg',
        },
    }
