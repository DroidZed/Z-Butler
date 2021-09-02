from config.main import color

no_perms_config = {
    "title": "You SUSSY BAKA !",
    "url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
    "description": "You're not powerful enough to use this command, how pifitul 😒",
    "color": color,
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
        "strike": {
            "text": "Next time make sure you have enough permissions, what a shame 🤐",
            "url": "https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif"
        },
        "kick": {
            "text": "You are not cool enough for this 🥱",
            "url": "https://emojis.slackmojis.com/emojis/images/1620894162/38676/kicking.gif"
        },
        "purge": {
            "text": "Cleaning behind you mess ? What a dog...🤮",
            "url": "https://emojis.slackmojis.com/emojis/images/1472329131/1120/nuclear-bomb.gif"
        }

    }
}

ban_config = {
    "title": "YOU HAVE BEEN BANNED",
    "url": "https://media1.tenor.com/images/0dcb84c900e10b6272152cd759eb1eab/tenor.gif",
    "description": "After the actions you've done in my server the admin decided to ban you for the safety of our community.",
    "color": color,
    "image_url": "https://media1.tenor.com/images/0dcb84c900e10b6272152cd759eb1eab/tenor.gif",
    "author": {
        "name": "The Z Butler",
        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
    "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
    "footer": {
        "text": "Next time think twice before making trouble in a server 😶",
        "url": "https://emoji.gg/assets/emoji/3886_BAN.gif"}}


def strike_config(number_of_strikes_left: int):
    return {
        "title": "YOU GOT A STRIKE, MIND YOUR OWN BUSINESS NEXT TIME.",
        "url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
        "description": "HOLD UP THERE ! BAD THINGS ARE NOT ALLOWED HERE, DO IT ELSEWHERE OR FACE THE CONSEQUENCES !",
        "color": color,
        "image_url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "footer": {
            "text": f"{number_of_strikes_left} Strikes and you're banned.",
            "url": "https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif?1542340473"}}


def pfp_config(url: str, tag: str, issuer: str, avatar_url: str) -> dict:
    res = {
        "title": f"**{tag}**'s Profile Picture",
        "color": color,
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


def gif_config(url: str, issuer: str, avatar_url: str, gif_name: str, tenor_link: str) -> dict:
    return {
        "title": f"**{gif_name}**",
        "color": color,
        "description": f"Original image link: [here]({tenor_link})",
        "image_url": f'{url}',
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "url": f"{avatar_url}"}}


def leave_config(username: str, id: int) -> dict:
    return {
        "title": f"{username} Left us.",
        "color": color,
        "description": f"<@{id}> got sucked into a blackhole <a:black_hole:796434656605765632>, long forgotten.",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"},
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "footer": {
            "text": f"We shall never remember those who left our cause.",
            "url": f"https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"}
    }


def how_gay(username: str, mention: str, rate: int, msg: str) -> dict:

    return {
        "title": f"{username}'s Gay Level",
        "color": color,
        "description": f"**{mention} is {rate}% gay** 🏳️‍🌈\n{msg}",
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        }
    }


def help_config() -> dict:

    return {
        "title": f"Help Command",
        "color": color,
        "description": "Showing you the list of my powers, write Zhelp <command name> | <category name> for more info on those.",
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        },
        'footer': {
            'text': 'Commands provided by The Z Butler 💙',
            'url': 'https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg'
        }

    }
