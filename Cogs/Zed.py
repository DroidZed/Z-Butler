from random import choice

from discord.ext.commands import Bot, Cog, Context, command, cooldown, BucketType

from config.embed.env_cfg import env_config
from config.main import PREFIX, OWNER_ID
from functions.embed_factory import create_embed


class ZedCog(Cog, name="Zed-Domain[WIP]", description="⚡ Domain expansion !"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="Z",
        description="Calls the bot. This command is a work in progress.",
        usage=f"{PREFIX}",
        aliases=[""],
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
            await ctx.message.reply("Hello master 😍", mention_author=True)
            return

        await ctx.message.reply(choice([choice(replies), choice(replies)]), mention_author=True)

    @command(name="env", description="Displays the bot's environment", usage=f"{PREFIX}env")
    async def env(self, ctx: Context):

        await ctx.send(embed=create_embed(env_config(), None, None))

    @command(name="say", description="Say something :/", usage=f"{PREFIX}say `your message`")
    async def say(self, ctx: Context, *msg: str):

        await ctx.message.delete()

        await ctx.send(f"{' '.join(msg)}")

    @command(
        name="python",
        aliases=["py"],
        description="Python is superior 🐍",
        usage=f"{PREFIX}py",
    )
    async def python(self, ctx: Context):

        await ctx.message.delete()

        await ctx.send(
            choice(
                [
                    "https://tenor.com/view/python-gif-20799882",
                    "https://tenor.com/view/java-python-fight-me-saber-tdfw-gif-16168791",
                    "https://tenor.com/view/dark-shadows-snake-python-hiss-gif-5700618",
                    "https://i.imgflip.com/44s4sh.jpg",
                    "https://i.imgflip.com/416iip.jpg",
                    "https://i.imgflip.com/1fv76g.jpg",
                ]
            )
        )


def setup(bot: Bot):
    bot.add_cog(ZedCog(bot))
