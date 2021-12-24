from util.colors import BOT_COLOR


def gif_config(url: str,
               issuer: str,
               avatar_url: str,
               gif_name: str,
               tenor_link: str) -> dict:
    return {
        "title": f"**{'NOICE 😏' if gif_name == '69' else gif_name}**",
        "color": BOT_COLOR,
        "description": f"Original image link: [here]({tenor_link})",
        "image": {"url": f'{url}'},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"},
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "icon_url": f"{avatar_url}"}
    }
