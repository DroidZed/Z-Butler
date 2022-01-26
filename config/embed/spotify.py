from util.colors import SPOTIFY_COLOR


def spotify_config(mention: str, song: str, album: str, artist: str, art: str, link: str) -> dict:
    return {
        "title": f"**{song}**",
        "color": SPOTIFY_COLOR,
        "description": f"{mention} is listening to this song by _{artist}_\nFrom the album **{album}**."
        f"\n Check it out -> [link]({link})",
        "image": {"url": f"{art}"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": "Songs params provided by Spotify 💚",
            "icon_url": "https://1000logos.net/wp-content/uploads/2017/08/Spotify-Logo.png",
        },
    }
