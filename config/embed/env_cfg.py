from platform import python_version

from discord import __version__

from util.colors import BOT_COLOR


def env_config() -> dict:
    return {
        "title": "Working Environment",
        "description": f"I'm working under the **latest** and **greatest** of :"
                       f"\n <:python:880768802885885973> `Python`: `{python_version()}`"
                       f"\n <:pycord:895264837284790283> `Pycord`: `{__version__}`",
        "color": BOT_COLOR,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"},
    }
