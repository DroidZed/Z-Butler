no_perms_config = {
    "title": "You SUSSY BAKA !",
    "url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
    "description": "You're not powerful enough to use this command, how pifitul 😒",
    "color": 0x0027b3,
    "image_url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
    "author": {
        "name": "The Z Butler",
        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
    },
    "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
    "footer": {
        "ban": {
            "text": "How funny...the admin shuold see this 😶",
            "url": "https://emoji.gg/assets/emoji/3886_BAN.gif"
        },
        "warn": {
            "text": "Next time make sure you have enough permissions, what a shame 🤐",
            "url": "https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif?1542340473"
        },
        "kick": {
            "text": "You are not cool enough for this 🥱",
            "url": "https://emojis.slackmojis.com/emojis/images/1620894162/38676/kicking.gif"
        }

    }
}

ban_config = {
    "title": "YOU HAVE BEEN BANNED",
    "url": "https://media1.tenor.com/images/0dcb84c900e10b6272152cd759eb1eab/tenor.gif",
    "description": "After the actions you've done in my server the admin decided to ban you for the safety of our community.",
    "color": 0x0027b3,
    "image_url": "https://media1.tenor.com/images/0dcb84c900e10b6272152cd759eb1eab/tenor.gif",
    "author": {
        "name": "The Z Butler",
        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
    },
    "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
    "footer": {
        "text": "Next time think twice before making trouble in a server 😶",
        "url": "https://emoji.gg/assets/emoji/3886_BAN.gif"
    }
}


def strike_config(number_of_strikes_left: int):
    return {
        "title": "YOU GOT A STIKE, MIND YOUR OWN BUSINESS NEXT TIME.",
        "url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
        "description": "HOLD UP THERE ! BAD THINGS ARE NOT ALLOWED HERE, DO IT ELSEWHERE OR FACE THE CONSEQUENCES !",
        "color": 0x0027b3,
        "image_url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        },
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "footer": {
            "text": f"{number_of_strikes_left} Strikes and you're banned.",
            "url": "https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif?1542340473"
        }
    }
