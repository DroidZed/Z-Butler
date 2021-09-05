from test import eight_ball_api
import time
from json import loads
from random import choice
from random import randint as rdn

from config.embed.gif import gif_config
from config.embed.how_gay import how_gay_config
from config.main import TENOR_KEY, PREFIX
from discord import Member
from discord.ext.commands import (Bot, BucketType, Cog, Context, command,
                                  cooldown)
from functions.embed_factory import create_embed
from requests import get


class FunCog(
        Cog,
        name="Fun Commands",
        description="Fun commands from your trusty Z Butler 💙"):

    def __init__(self, bot):
        self.bot = bot

    @command(name='SUS',
             usage=f"{PREFIX}SUS `username`",
             description="I think we got an imposter among us...",
             aliases=['sus', 'amogus', 'imposter'])
    @cooldown(1, 5, BucketType.user)
    async def SUS(self, ctx: Context, member: Member = None) -> None:
        member = member or ctx.message.author

        t = f".      　。　　　　•　    　  ﾟ　　    。"
        t2 = ".　　　.　　　  　　.　　　　　。　　     。　."
        t3 = ".　　      。　        ඞ   。　    .      •"
        t4 = f".      {member.mention} was The Imposter.　 。　."
        t5 = "　 　　。　　　　　　ﾟ　　　.　　　　　."
        t6 = ",         .　         .　　       ."

        final = f"{t2}\n{t3}\n{t4}\n{t5}\n{t6}"

        await ctx.send(final)

    @command(name="gif_search",
             usage=f"{PREFIX}gif_search query",
             description="Look for a gif about a certain topic",
             aliases=['gif?']
             )
    @cooldown(1, 15, BucketType.user)
    async def look_for_gif(self, ctx: Context, *query: str) -> None:
        limit = 100

        topic = " ".join(query)

        r = get("https://g.tenor.com/v1/search", {
                'q': topic,
                'key': TENOR_KEY,
                'limit': limit
                })

        if r.status_code == 200:
            data = loads(r.content)
            result_set = choice(data['results'])
            await ctx.send(
                embed=create_embed(
                    config=gif_config(url=result_set['media'][0]['gif']['url'],
                                      issuer=ctx.message.author.name,
                                      avatar_url=ctx.message.author.avatar_url,
                                      gif_name=topic,
                                      tenor_link=result_set['url'])))
        else:
            await ctx.send(content=f"No GIF found for the topic {topic}")
            return

    @command(
        name="ping",
        usage=f"{PREFIX}ping",
        description="Show the bot's ping.")
    @cooldown(1, 2, BucketType.member)
    async def ping(self, ctx) -> None:
        before = time.monotonic()

        message = await ctx.send("🏓 Pong !")

        ping = (time.monotonic() - before) * 1000

        await message.edit(content=f"🏓 Pong !  `{int(ping)} ms`")

    @command(
        name="howgay",
        usage=f"{PREFIX}howgay `username`",
        description="Checks how gay a user is, ew...",
        aliases=['hg'])
    async def how_gay(self, ctx: Context, member: Member = None) -> None:

        if member is None:
            member = ctx.author

        rate = rdn(0, 100)

        msg = self._gay_commentary(rate)

        config = how_gay_config(username=member.name,
                                mention=member.mention,
                                rate=rate,
                                msg=msg)

        if rate > 65:

            config['image_url'] = "https://c.tenor.com/GTjxHh4xr2kAAAAC/you-are-an-abomination-creature.gif"

        embed = create_embed(config=config)

        await ctx.send(embed=embed)

    def _gay_commentary(self, rate: int) -> str:

        if not rate:
            return "That's a real human 😉"

        elif rate < 10:
            return "Need purifying 😬"

        elif rate < 50:
            return 'What a shame...🙄'

        elif rate < 65:
            return 'Utterly disgusting...🤮'
        else:
            return '**YOU ARE AN ABOMINATION, YOU HAVE NO RIGHT TO LIVE !! DIE YOU MONSTER !!**'

    @command(
        name="8ball",
        usage=f"{PREFIX}8ball `question`",
        description="Ask the magical 8 ball about anything.",
        aliases=['8b'])
    async def _8_ball(self, ctx: Context, *question: str) -> None:

        if not question:
            await ctx.send("No question provided 🙄")
        else:
            qst = " ".join(question)
            api: dict = await eight_ball_api(qst)
            await ctx.send(api['body']['answer'])


def setup(bot: Bot):
    bot.add_cog(FunCog(Cog))
