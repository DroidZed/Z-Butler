from util.colors import TWITTER_COLOR


def tweet_config(text: str, t_id: int, username: str):

    return {
        "title": f"The bird tweets",
        "url": f"https://twitter.com/{username}/status/{t_id}",
        "color": TWITTER_COLOR,
        "description": text,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": f"Tweeted by {username} - id: {t_id}",
            "icon_url": "https://www.brandcolorcode.com/media/twitter-logo.png",
        },
    }
