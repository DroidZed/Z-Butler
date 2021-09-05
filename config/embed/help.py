from config.main import COLOR


def help_config(title: str = None, desc: str = None) -> dict:

    return {
        "title": title or "Help Command",
        "color": COLOR,
        "description": desc or "Showing you the list of my powers, write Zhelp <command name> | <category name> for more info on those.",
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        },
        'footer': {
            'text': 'The power of The Z Butler 🔱',
            'url': 'https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg'
        }

    }
