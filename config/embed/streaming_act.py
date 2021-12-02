from util.colors import TWITCH_PURPLE, BOT_COLOR, YOUTUBE_RED


def streaming_activity_config(name: str,
                              mention: str,
                              issuer: str,
                              avatar_url: str,
                              platform: str,
                              streamer_pfp: str = None,
                              stream_url: str = None,
                              streamed_game: str = None) -> dict:
    dic = {
        "title": f"{name}",
        "description": f"{mention} is `streaming` ***this*** 👻",
        "color": __change_platform_color(platform),
        "url": "",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "image": {"url": ""},
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "icon_url": f"{avatar_url}"
        }
    }

    if stream_url:
        dic["description"] += f"\nFollow this [link]({stream_url}) to catch them **live** 🔴 on `{platform}` !"

    if streamed_game:
        dic["description"] = dic["description"].replace(
            "this", f"{streamed_game}")

    if streamer_pfp:
        dic["url"] = f"{stream_url}",
        dic["image"] = {
            "url": f"{streamer_pfp}"
        }

    return dic


def __change_platform_color(platform: str) -> int:
    if platform == 'Twitch':
        return TWITCH_PURPLE
    elif platform == 'YouTube':
        return YOUTUBE_RED
    else:
        return BOT_COLOR
