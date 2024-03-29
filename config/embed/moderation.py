from config.colors import BOT_COLOR, CROWN_COLOR


def kick_config(message: str) -> dict:
    return {
        "description": message,
        "color": CROWN_COLOR,
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
    }


def mute_config(member_id: int) -> dict:
    return {
        "title": "The hammer has fallen",
        "color": BOT_COLOR,
        "description": f"Muted <@{member_id}>. Take the time to seek help.",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "footer": {
            "text": "Dragon's Heart Team.",
            "icon_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        },
    }


def ban_config():
    return {
        "title": "YOU HAVE BEEN BANNED",
        "url": "https://media1.tenor.com/images/0dcb84c900e10b6272152cd759eb1eab/tenor.gif",
        "description": "After the actions you've done in my server the admin decided to ban you for the safety of our "
        "community.",
        "color": CROWN_COLOR,
        "image": {"url": "https://media1.tenor.com/images/0dcb84c900e10b6272152cd759eb1eab/tenor.gif"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "footer": {
            "text": "Next time think twice before making trouble in a server 😶",
            "icon_url": "https://emoji.gg/assets/emoji/3886_BAN.gif",
        },
    }


def unmute_config(member_id: int) -> dict:
    return {
        "title": "Forgiveness is a choice",
        "color": BOT_COLOR,
        "description": f"Unmuted <@{member_id}>. Hopefully you've reflected on your actions.",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": "Dragon's Heart Team.",
            "icon_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        },
    }


def strike_config(number_of_strikes_left: int):
    return {
        "title": "YOU GOT A STRIKE, MIND YOUR OWN BUSINESS NEXT TIME.",
        "url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
        "description": "HOLD UP THERE ! BAD THINGS ARE NOT ALLOWED HERE, DO IT ELSEWHERE OR FACE THE CONSEQUENCES !",
        "color": CROWN_COLOR,
        "image": {"url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "text": f"{number_of_strikes_left} Strikes and you're banned.",
            "icon_url": "https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif?1542340473",
        },
    }


def no_perms_config():
    return {
        "title": "You SUSSY BAKA !",
        "url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
        "description": "You're not powerful enough to use this command, how pitiful 😒",
        "color": BOT_COLOR,
        "image": {"url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif"},
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
        },
        "thumbnail": {
            "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
        },
        "footer": {
            "ban": {
                "text": "How funny...the admin should see this 😶",
                "icon_url": "https://emoji.gg/assets/emoji/3886_BAN.gif",
            },
            "strike": {
                "text": "Next time make sure you have enough permissions, what a shame 🤐",
                "icon_url": "https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif",
            },
            "kick": {
                "text": "You are not cool enough for this 🥱",
                "icon_url": "https://emojis.slackmojis.com/emojis/images/1620894162/38676/kicking.gif",
            },
            "purge": {
                "text": "Cleaning behind you mess ? What a dog...🤮",
                "icon_url": "https://emojis.slackmojis.com/emojis/images/1472329131/1120/nuclear-bomb.gif",
            },
            "mute": {
                "text": "Shushing your own kin ? You dumb bro ?",
                "icon_url": "https://c.tenor.com/_g7PgSa_6vIAAAAS/speechless-mute.gif",
            },
            "unmute": {
                "text": "The silenced shall remain unheard of, buried under the misery of their own mistakes.",
                "icon_url": "https://c.tenor.com/lXqsq1j6KTUAAAAS/matrix-mouth.gif",
            },
        },
    }
