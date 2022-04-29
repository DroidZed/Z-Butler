from util.colors import BOT_COLOR


def mute_config(member_id: int) -> dict:
    return {
        "title": f"The hammer has fallen",
        "color": BOT_COLOR,
        "description": f"Muted <@{member_id}>. Take the time to seek help.",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": "Dragon's Heart Team.",
            "icon_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        },
    }


def unmute_config(member_id: int) -> dict:
    return {
        "title": f"Forgiveness is a choice",
        "color": BOT_COLOR,
        "description": f"Unmuted <@{member_id}>. Hopefully you've reflected on your actions.",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": "Dragon's Heart Team.",
            "icon_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        },
    }
