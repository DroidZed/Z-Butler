from platform import python_version
from random import choice

from discord import __version__
from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
    cooldown,
    BucketType,
    CommandError,
    BadBoolArgument,
)

from api.images import find_gif
from classes.embed_factory import EmbedFactory
from config.colors import BOT_COLOR
from config.main import PREFIX, OWNER_ID

from classes.embedder_machine import (
    EmbedderMachine,
    Zembed,
    ZembedField,
)


class ZedCog(
    Cog,
    name="Zed-Domain[WIP]",
    description="⚡ Domain expansion !",
):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="Z",
        description="Calls the bot. This command is a work in progress.",
        usage=f"{PREFIX}",
    )
    @cooldown(1, 2.5, BucketType.user)
    async def zed(self, ctx: Context):
        replies = [
            "WHAT ?!",
            "What do you need ?",
            "I'm busy attending to the server, move along...",
            "Don't bother me you stupid !",
            "Go out there and touch some grass !!",
            "Shouldn't you be outside finding a partner instead ? You miserable virgin !!",
            "I bet your parents aren't proud of you and your gf/bf thinks you're a boring little clamp !",
        ]

        if ctx.author.id == OWNER_ID:
            await ctx.message.reply(
                "Hello master 😍", mention_author=True
            )
            return

        await ctx.message.reply(
            choice([choice(replies), choice(replies)]),
            mention_author=True,
        )

    @command(
        name="env",
        description="Displays the bot's environment",
        usage=f"{PREFIX}env",
    )
    async def env(self, ctx: Context):

        machine = EmbedderMachine()

        machine.set_embed_components(
            title="Working Environment",
            color=BOT_COLOR,
            description="I'm working under the **latest** and **greatest** of"
            f"\n <:python:1071060794759970867> `Python`: `{python_version()}`"
            f"\n <:pycord:1071060792721555538> `Pycord`: `{__version__}`",
            author_name="The Z Butler",
            author_image="https://cdn.discordapp.com/avatars/759844892443672586"
            "/bb7df4730c048faacd8db6dd99291cdb.jpg",
        )

        await ctx.send(embed=machine.embed)

    @command(
        name="say",
        description="Say something :/",
        usage=f"{PREFIX}say `True` | `False` `your message`",
    )
    async def say(
        self,
        ctx: Context,
        with_author: bool = False,
        *msg: str,
    ):
        await ctx.message.delete()

        auth = (
            f"- *By {ctx.author.name}*"
            if with_author
            else ""
        )

        await ctx.send(f'{" ".join(msg)} {auth}')

    @command(
        name="python",
        aliases=["py"],
        description="Python is superior 🐍",
        usage=f"{PREFIX}py",
    )
    async def python(self, ctx: Context):
        await ctx.message.delete()

        async with ctx.typing():
            gif = await find_gif("python")

        await ctx.send(
            choice(
                [
                    gif["url"]
                    if gif
                    else choice(
                        [
                            "https://tenor.com/view/python-gif-20799882",
                            "https://tenor.com/view/java-python-fight-me-saber-tdfw-gif-16168791",
                            "https://tenor.com/view/dark-shadows-snake-python-hiss-gif-5700618",
                        ]
                    ),
                    "https://i.imgflip.com/44s4sh.jpg",
                    "https://i.imgflip.com/416iip.jpg",
                    "https://i.imgflip.com/1fv76g.jpg",
                ]
            )
        )

    @say.error
    async def say_handler(
        self, ctx: Context, error: CommandError
    ) -> None:

        if isinstance(error, BadBoolArgument):
            await ctx.reply(
                "Please provide the correct argument for writing the signature."
            )

        else:
            await ctx.reply(
                "Check the command's help page for the correct syntax."
            )


def setup(bot: Bot):
    bot.add_cog(ZedCog(bot))
