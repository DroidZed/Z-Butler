from discord import Embed

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
    "color": color,
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
        "title": "YOU GOT A STRIKE, MIND YOUR OWN BUSINESS NEXT TIME.",
        "url": "https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
        "description": "HOLD UP THERE ! BAD THINGS ARE NOT ALLOWED HERE, DO IT ELSEWHERE OR FACE THE CONSEQUENCES !",
        "color": color,
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


def pfp_config(url: str, tag: str, issuer: str) -> dict:
    return {
        "title": f"**{tag}**'s Profile Picture",
        "color": color,
        "image_url": f'{url}',
        "author": {
            "name": "The Z Butler",
            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        },
        "thumbnail_url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif",
        "footer": {
            "text": f"Requested by {issuer} 💙",
            "url": "https://cdn.discordapp.com/emojis/765999349008039936.png?v=1"
        }
    }


def createEmbed(config: dict, reason: str = None, action: str = None, no_perms_type: str = None) -> Embed:

    if ('url' in config) & ('description' in config):
        embed = Embed(
            title=config['title'],
            url=config['url'],
            description=config['description'],
            color=config['color']
        )
    else:
        embed = Embed(
            title=config['title'],
            color=config['color']
        )

    embed.set_author(
        name=config['author']['name'],
        icon_url=config['author']['icon_url']
    )

    if action is not None:
        embed.add_field(
            name="Action",
            value=action,
            inline=True
        )

    embed.set_thumbnail(
        url=config["thumbnail_url"]
    )

    if reason is not None:
        embed.add_field(
            name="Reason",
            value=reason if reason else "No reason given",
            inline=True
        )

    if 'image_url' in config:
        embed.set_image(url=config["image_url"])

    if config is no_perms_config and no_perms_type is not None:

        embed.set_footer(
            text=config['footer'][no_perms_type]['text'],
            icon_url=config['footer'][no_perms_type]['url']
        )
    else:
        embed.set_footer(
            text=config['footer']['text'],
            icon_url=config['footer']['url']
        )

    return embed
