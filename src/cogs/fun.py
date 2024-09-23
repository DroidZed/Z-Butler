import time
from asyncio import sleep
from random import choice
from typing import Optional

from discord import Member, Message, User
from discord.ext.commands import (
    Bot,
    BucketType,
    Cog,
    Context,
    command,
    cooldown,
)
from modules.animals_api import (
    AnimalsAPI,
    CatFact,
    DocPicture,
)
from modules.embedder import (
    EmbedderMachine,
    ZembedField,
    generate_embed,
)
from modules.tenor_api import TenorAPI
from utils import Env


class FunCog(
    Cog,
    name="Fun",
    description="🎉 Fun commands from your trusty Z Butler 💙",
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.tenor_api = TenorAPI()
        self.animals_api = AnimalsAPI()

    @command(
        name="SUS",
        usage=f"{Env.PREFIX}SUS `username`",
        description="I think we got an imposter among us...",
        aliases=["sus", "amogus", "imposter"],
    )
    @cooldown(1, 5, BucketType.user)
    async def sus(
        self,
        ctx: Context,
        member: Optional[Member | User] = None,
    ):
        member = member or ctx.message.author

        await ctx.message.delete()

        await ctx.send(
            f""".      　。　　　　•　    　  ﾟ　　    。
        .　　　.　　　  　　.　　　　　。　　     。　.
        .　　      。　        ඞ   。　    .      •
        .      {member.mention} was The Imposter.　 。　.
        　 　　。　　　　　　ﾟ　　　.　　　　　.
        ,         .　         .　　       ."""
        )

    @command(
        name="gif_search",
        usage=f"{Env.PREFIX}gif_search `query`",
        description="Look for a gif about a certain topic",
        aliases=["gif?"],
    )
    @cooldown(1, 15, BucketType.user)
    async def look_for_gif(self, ctx: Context, *query: str):
        topic = " ".join(query)

        async with ctx.typing():
            link = await self.tenor_api.find_gif(topic)

        if isinstance(link, str):
            return await ctx.send(
                embed=generate_embed(
                    title=f"**{'NOICE 😏' if topic == '69' else topic}**",
                    image_url=f"{link}",
                    footer_text=f"Requested by {ctx.message.author.name} 💙",
                    footer_icon=f"{ctx.message.author.display_avatar.url}",
                )
            )

        else:
            return await ctx.send(content=f"No GIF found for the topic {topic}")

    @command(
        name="ping",
        usage=f"{Env.PREFIX}ping",
        description="Show the bot's ping.",
    )
    @cooldown(1, 2, BucketType.member)
    async def ping(self, ctx: Context):
        await ctx.message.delete()

        start_time = time.time()

        machine = EmbedderMachine()

        machine.set_embed_components(
            title="Z Butler's Ping",
            description="🏓 Ping !",
            image_url="https://c.tenor.com/ptYJsG8-K4MAAAAC/cats-ping-pong.gif",
        )

        machine.add_footer(
            footer_text=f"Requested by {ctx.message.author.name} 💙",
            footer_icon=f"{ctx.message.author.display_avatar.url}",
        )

        message: Message = await ctx.send(embed=machine.embed)

        end_time = time.time()

        machine.set_embed_components(
            description="🏓 Pong !",
        )

        machine.add_fields(
            ZembedField(
                inline=True,
                name="API",
                value=f"`{round((end_time - start_time) * 1000)}ms`",
            ),
            ZembedField(
                inline=True,
                name="Bot Latency",
                value=f"`{round(self.bot.latency * 1000)}ms`",
            ),
        )

        return await message.edit(embed=machine.embed)

    @command(
        name="8ball",
        usage=f"{Env.PREFIX}8ball `question`",
        description="Ask the magical 8 ball about anything.",
        aliases=["8b"],
    )
    @cooldown(1, 5, BucketType.member)
    async def _8_ball(self, ctx: Context, *question: str):
        if not question:
            return await ctx.send("No question provided 🙄")

        machine = EmbedderMachine()

        machine.set_embed_components(
            title="8-Ball Game 🎱",
            description="Thinking...",
            image_url="https://media.tenor.com/images/67155da2720fa29220200465f1a4bd84/tenor.gif",
        )

        machine.add_footer(
            footer_icon="https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
            footer_text="8Ball by Z Butler 💙",
        )

        message: Message = await ctx.send(embed=machine.embed)

        async with ctx.typing():
            answer = eight_ball_answers()
            await sleep(4)

        machine.set_embed_components(
            title="8-Ball Game 🎱",
            description=f"{ctx.message.author.mention}, your answer is: ***__{answer}__***",
        )

        machine.remove_image()

        await message.edit(embed=machine.embed)

    @command(
        name="hug",
        usage=f"{Env.PREFIX}hug `username`",
        description="Give someone some a hug !!",
    )
    @cooldown(1, 2, BucketType.user)
    async def hug(
        self,
        ctx: Context,
        member: Optional[Member | User] = None,
    ):
        member = member or ctx.author()

        async with ctx.typing():
            gif = await self.tenor_api.find_gif("hug anime")

        if not isinstance(gif, str):
            return await ctx.send("Couldn't send the hug :(")

        await ctx.send(
            embed=generate_embed(
                title=f"{member.name} I send you a hug by {ctx.author.name} ❤",
                image_url=gif,
                footer_text=f"Requested by {ctx.message.author.name} 💙",
                footer_icon=f"{ctx.message.author.display_avatar.url}",
            )
        )

    @command(
        name="randomCatFact",
        usage=f"{Env.PREFIX}rcf",
        description="Sends a random cat fact",
        aliases=["rcf"],
    )
    @cooldown(1, 2, BucketType.user)
    async def random_cat_facts(self, ctx: Context):
        async with ctx.typing():
            res = await self.animals_api.get_random_cat_facts()

        if not isinstance(res, CatFact):
            return await ctx.send("Unable to pursue the request, the API failed.")

        await ctx.send(
            embed=generate_embed(
                title="Cat facts",
                description=f"*{res.fact}*",
            )
        )

    @command(
        name="doggoPics",
        usage=f"{Env.PREFIX}rdp",
        description="Sends a random dog pic",
        aliases=["rdp"],
    )
    @cooldown(1, 2, BucketType.user)
    async def random_dog_pics(self, ctx: Context):
        async with ctx.typing():
            res = await self.animals_api.get_random_dog_picture()

        if not isinstance(res, DocPicture) or res.status != "success":
            return await ctx.send("Unable to pursue the request, the API failed.")

        await ctx.send(embed=generate_embed(image_url=res.message))


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


def setup(bot: Bot):
    bot.add_cog(FunCog(bot))
