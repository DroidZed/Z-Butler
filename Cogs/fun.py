import time
from asyncio import sleep
from random import randint as rdn

from discord import Message
from discord.ext.commands import (
    Bot,
    BucketType,
    Cog,
    Context,
    MemberConverter,
    command,
    cooldown,
)

from api.animals import get_random_cat_facts, get_random_dog_picture
from api.images import find_gif
from classes.embed_factory import EmbedFactory
from config.colors import BOT_COLOR
from config.main import PREFIX
from functions.helpers import gay_commentary, eight_ball_answers


class FunCog(Cog, name="Fun", description="🎉 Fun commands from your trusty Z Butler 💙"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="SUS",
        usage=f"{PREFIX}SUS `username`",
        description="I think we got an imposter among us...",
        aliases=["sus", "amogus", "imposter"],
    )
    @cooldown(1, 5, BucketType.user)
    async def sus(self, ctx: Context, member: MemberConverter = None) -> None:
        member = member or ctx.message.author

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
        usage=f"{PREFIX}gif_search `query`",
        description="Look for a gif about a certain topic",
        aliases=["gif?"],
    )
    @cooldown(1, 15, BucketType.user)
    async def look_for_gif(self, ctx: Context, *query: str) -> None:

        topic = " ".join(query)

        async with ctx.typing():
            result_set = await find_gif(topic)

        if result_set:
            await ctx.send(
                embed=EmbedFactory.create_embed(
                    config=EmbedFactory.create_config(
                        title=f"**{'NOICE 😏' if topic == '69' else topic}**",
                        color=BOT_COLOR,
                        image={"url": f"{result_set['media'][0]['gif']['url']}"},
                        author={
                            "name": "The Z Butler",
                            "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                        },
                        footer={
                            "text": f"Requested by {ctx.message.author.name} 💙",
                            "icon_url": f"{ctx.message.author.avatar_url}",
                        },
                    )
                )
            )
        else:
            await ctx.send(content=f"No GIF found for the topic {topic}")
            return

    @command(name="ping", usage=f"{PREFIX}ping", description="Show the bot's ping.")
    @cooldown(1, 2, BucketType.member)
    async def ping(self, ctx: Context) -> None:

        await ctx.message.delete()

        start_time = time.time()

        message: Message = await ctx.send(
            embed=EmbedFactory.create_embed(
                cfg_type="ping",
                config=EmbedFactory.create_config(
                    title="Z Butler's Ping",
                    color=BOT_COLOR,
                    description="🏓 Pong !",
                    image={"url": "https://c.tenor.com/ptYJsG8-K4MAAAAC/cats-ping-pong.gif"},
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={
                        "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
                    },
                ),
            )
        )

        end_time = time.time()

        await message.edit(
            embed=EmbedFactory.create_embed(
                cfg_type="ping",
                config=EmbedFactory.create_config(
                    title="Z Butler's Ping",
                    color=BOT_COLOR,
                    description="🏓 Pong !",
                    image={"url": "https://c.tenor.com/ptYJsG8-K4MAAAAC/cats-ping-pong.gif"},
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={
                        "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
                    },
                ),
                **{
                    "API": f"`{round((end_time - start_time) * 1000)}ms`",
                    "Bot Latency": f"`{round(self.bot.latency * 1000)}ms`",
                },
            )
        )

    @command(
        name="howgay",
        usage=f"{PREFIX}howgay `username`",
        description="Checks how gay a user is, ew...",
        aliases=["hg", "hg?"],
    )
    async def how_gay(self, ctx: Context, member: MemberConverter = None) -> None:

        member = member or ctx.author

        async with ctx.typing():
            rate = rdn(0, 100)

            msg = gay_commentary(rate)

        await ctx.send(
            embed=EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    title=f"{member.name}'s Gay Level",
                    color=BOT_COLOR,
                    description=f"**{member.mention} is {rate}% gay** 🏳️‍🌈\n{msg}",
                    image={
                        "url": (
                            "https://tenor.com/view/disappointed-zac-efron-im-not-mad-upset-hurt-gif-14717203"
                            if rate < 69
                            else "https://c.tenor.com/GTjxHh4xr2kAAAAC/you-are-an-abomination-creature.gif"
                        )
                    },
                    thumbnail={
                        "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
                    },
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                )
            )
        )

    @command(
        name="8ball",
        usage=f"{PREFIX}8ball `question`",
        description="Ask the magical 8 ball about anything.",
        aliases=["8b"],
    )
    @cooldown(1, 5, BucketType.member)
    async def _8_ball(self, ctx: Context, *question: str) -> None:

        if not question:
            await ctx.send("No question provided 🙄")
            return

        message: Message = await ctx.send(
            embed=EmbedFactory.create_embed(
                EmbedFactory.create_config(
                    title=f"**8-Ball Game**",
                    color=BOT_COLOR,
                    description="Thinking...",
                    image={"url": "https://media.tenor.com/images/67155da2720fa29220200465f1a4bd84/tenor.gif"},
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    footer={
                        "text": "Requested by Z Butler 💙",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                )
            )
        )

        async with ctx.typing():
            answer = eight_ball_answers()
            await sleep(4)

        await message.edit(
            embed=EmbedFactory.create_embed(
                EmbedFactory.create_config(
                    title="8-Ball Game 🎱",
                    color=BOT_COLOR,
                    description=f"{ctx.message.author.mention}, your answer is: ***__{answer}__***",
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={
                        "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
                    },
                )
            )
        )

    @command(
        name="hug",
        usage=f"{PREFIX}hug `username`",
        description="Give someone some a hug !!",
    )
    @cooldown(1, 2, BucketType.user)
    async def hug(self, ctx: Context, member: MemberConverter = None) -> None:

        member = member or ctx.author

        async with ctx.typing():
            gif = await find_gif("hug anime")

        if not gif:
            await ctx.send("Couldn't send the hug :(")
            return

        await ctx.send(
            embed=EmbedFactory.create_embed(
                EmbedFactory.create_config(
                    title=f"{member.name} I send you a hug by {ctx.author.name} ❤",
                    color=BOT_COLOR,
                    image={"url": f"{gif['media'][0]['gif']['url']}"},
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    footer={
                        "text": f"Requested by {ctx.message.author.name} 💙",
                        "icon_url": f"{ctx.message.author.avatar_url}",
                    },
                )
            )
        )

    @command(name="randomCatFact", usage=f"{PREFIX}rcf", description="Sends a random cat fact", aliases=["rcf"])
    @cooldown(1, 2, BucketType.user)
    async def random_cat_facts(self, ctx: Context):

        async with ctx.typing():
            res = await get_random_cat_facts()

        if not res:
            await ctx.send("Unable to persue the request, the API failed.")
            return

        await ctx.send(
            embed=EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    color=BOT_COLOR,
                    description=f"*{res['fact']}*",
                    author={
                        "name": "Random cat facts by The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={
                        "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
                    },
                )
            )
        )

    @command(name="doggoPics", usage=f"{PREFIX}rdp", description="Sends a random dog pic", aliases=["rdp"])
    @cooldown(1, 2, BucketType.user)
    async def random_dog_pics(self, ctx: Context):

        async with ctx.typing():
            res = await get_random_dog_picture()

            if not res or res["status"] != "success":
                await ctx.send("Unable to persue the request, the API failed.")
                return

        await ctx.send(
            embed=EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    color=BOT_COLOR,
                    image={"url": f"{res['message']}"},
                    author={
                        "name": "Random doggo pics by The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={
                        "url": "https://64.media.tumblr.com/fbeaedb718f8f4c23d261b100bbf62cc/tumblr_onv6j3by9b1uql2i0o1_500.gif"
                    },
                )
            )
        )


def setup(bot: Bot):
    bot.add_cog(FunCog(bot))
