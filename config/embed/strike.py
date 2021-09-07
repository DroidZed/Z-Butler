from config.main import COLOR


def strike_config(number_of_strikes_left: int):
    return {
        "title": "YOU GOT A STRIKE, MIND YOUR OWN BUSINESS NEXT TIME.",
        "url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
        "description": "HOLD UP THERE ! BAD THINGS ARE NOT ALLOWED HERE, DO IT ELSEWHERE OR FACE THE CONSEQUENCES !",
        "color": COLOR,
        "image": {"url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail": {"url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"},
        "footer": {
            "text": f"{number_of_strikes_left} Strikes and you're banned.",
            "icon_url": "https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif?1542340473"}
    }
