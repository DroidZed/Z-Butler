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


from modules.embedder.zembed_models import (
    ZembedField,
    Zembed,
)
from modules.embedder.embedder_machine import (
    EmbedderMachine,
)


def get_server_image(g: Optional[Guild]) -> Optional[str]:
    return g.icon.url if g and g.icon else None


def generate_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    color: Optional[int] = None,
    url: Optional[str] = None,
    thumbnail_url: Optional[str] = None,
    image_url: Optional[str] = None,
    footer_icon: Optional[str] = None,
    footer_text: Optional[str] = None,
    rem_img=False,
    *fields: ZembedField,
) -> Zembed:
    machine = EmbedderMachine()

    machine.set_embed_components(
        title,
        description,
        color,
        url,
        thumbnail_url,
        image_url,
    )

    if footer_icon and footer_text:
        machine.add_footer(footer_icon, footer_text)

    machine.add_fields(*fields)

    if rem_img:
        machine.remove_image

    return machine.embed


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


def extract_guild_data(
    roles: List[Role],
    members: List[Member],
    description: str,
):
    roles_count: int = len(roles) - 1

    online_users_count: int = len(
        list(
            filter(
                lambda member: member.status
                != Status.offline
                and not member.bot,
                members,
            )
        )
    )

    machines_count: int = len(
        list(filter(lambda member: member.bot, members))
    )

    return (
        roles_count,
        online_users_count,
        machines_count,
        description,
    )


def print_msg():
    print("/" * 39)
    print(" ----------\\")
    rch.print(
        " |       [b cyan]*[/]  |         [white]/[/]\\"
    )
    print(" --------   |        /  \\")
    print("       /   /         \\   \\")
    print("      /   /          /   /")
    rch.print(
        "     [white]/[/]   [white]/[/] [b blue]The Z Bot[/] \\   \\"
    )
    print("    |   --------------   /")
    rch.print(
        "    |       [b green]ONLINE[/]      [white]/[/]"
    )
    print("     ------------------")
    rch.print(
        f"|[b]         [i]By: [purple]DroidZed[/purple][/i]{' ' * 16}|"
    )
    rch.print(
        f"|[b] Discord version: [u blue]{version_info.major}.{version_info.minor}.{version_info.micro}[/u blue]{' ' * 14}|",
        end="\n",
    )
    rch.print(
        f"[b white]| Running under: [i yellow]Python v{python_version()}[/i yellow] :snake:    |",
        end="\n",
    )  # Don't remove the extra space added after the snake emoji, it was added so the bars will align in the console
    # of the hosting.
    print("/" * 39)
