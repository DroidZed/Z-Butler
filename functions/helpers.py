from random import choice

from discord import Guild, Status


def eight_ball_answers() -> str:
    answers = {
        "+": [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "Take the right, the road is yours !",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Signs point to yes.",
        ],
        "/": [
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "I don't really know..",
            "Clouded mind, can't think straight.",
            "Go for a walk, maybe that should clear your mind about the issue that troubles you.",
            "Drink water, pet an animal or talk to someone about it, I'm not your doctor.",
        ],
        "-": [
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
            "IMPOSSIBLE",
            "You're a fool to believe that !",
            "Ain't smart enough to figure it out eh ? Well guess what !! or don't, you're so stupid to even understand.",
            "A dark path is on the horizon, better go left.",
        ],
    }

    return choice(answers[choice(["+", "-", "/"])])

def extract_guild_data(guild: Guild):
    roles_count: int = len(guild.roles) - 1

    desc = guild.description

    online_users_count: int = len(
        list(
            filter(
                lambda member: member.status != Status.offline and not member.bot,
                guild.members,
            )
        )
    )

    machines_count: int = len(list(filter(lambda member: member.bot, guild.members)))

    return roles_count, online_users_count, machines_count, desc
