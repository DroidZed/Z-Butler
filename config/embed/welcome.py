from util.colors import BOT_COLOR


def welcome_config() -> dict:
    return {
        "title": f"Hello there fellow Dragon Warrior",
        "color": BOT_COLOR,
        "description": "Welcome to **DRAGON'S HEART** !! Please open a ticket in <#778292937426731049> and a member of the staff team will be with you shortly",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": "Your trusty bot Z 🔱",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
    }
