from util.colors import SPOTIFY_COLOR


def song_config(**data) -> dict:
    return {
        "title": f"**{data['title']}**",
        "url": data['song_url'],
        "color": SPOTIFY_COLOR,
        "description": f"The song you've requested, by {data['artist']}",
        "image": {"url": f"{data['art_url']}"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail": {
            "url":
                "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"},
        "footer": {
            "text": 'Songs data provided by Spotify 💚',
            "icon_url": "https://1000logos.net/wp-content/uploads/2017/08/Spotify-Logo.png",
        }
    }
