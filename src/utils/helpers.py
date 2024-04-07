from typing import Optional, List
from random import choice
from platform import python_version

import rich as rch
from discord import (
    version_info,
    Status,
    Role,
    Member,
    Guild,
)


def get_server_image(g: Optional[Guild]) -> Optional[str]:
    return g.icon.url if g and g.icon else None


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


def extract_guild_data(roles: List[Role], members: List[Member]):
    roles_count: int = len(roles) - 1

    online_users_count: int = len(
        list(
            filter(
                lambda member: member.status != Status.offline
                and member.status != Status.invisible
                and not member.bot,
                members,
            )
        )
    )

    machines_count: int = len(list(filter(lambda member: member.bot, members)))

    return (
        roles_count,
        online_users_count,
        machines_count,
    )


def print_msg():
    rch.print("/" * 39)
    rch.print(" ----------\\")
    rch.print(" |       [b cyan]*[/]  |         [white]/[/]\\")
    rch.print(" --------   |        /  \\")
    rch.print("       /   /         \\   \\")
    rch.print("      /   /          /   /")
    rch.print("     [white]/[/]   [white]/[/] [b blue]The Z Bot[/] \\   \\")
    rch.print("    |   --------------   /")
    rch.print("    |       [b green]ONLINE[/]      [white]/[/]")
    rch.print("     ------------------")
    rch.print(
        f"[b white]|[b]         [i]By: [purple]DroidZed[/purple][/i]{' ' * 16}|"
    )
    rch.print(
        f"[b white]|[b] Discord version: [u blue]{version_info.major}.{version_info.minor}.{version_info.micro if version_info.micro else 0}[/u blue]{' ' * 11}|",
        end="\n",
    )
    rch.print(
        f"[b white]| Running under: [i yellow]Python v{python_version()}[/i yellow] :snake:    |",
        end="\n",
    )  # Don't remove the extra space added after the snake emoji, it was added so the bars will align in the console
    # of the hosting.
    rch.print("/" * 39)


if __name__ == "__main__":
    print_msg()
