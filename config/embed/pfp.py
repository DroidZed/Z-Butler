from config.main import COLOR


def pfp_config(url: str, tag: str, issuer: str, avatar_url: str) -> dict:
    res = {
        "title": f"**{tag}**'s Profile Picture",
        "color": COLOR,
        "image_url": f'{url}',
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "url": f"{avatar_url}"}
    }
    if tag.split('#')[0] == 'DroidZed':
        res['title'] = f"Lord\t👑 **𝕯𝖗𝖔𝖎𝖉𝖅𝖊𝖉** 👑"
    return res
