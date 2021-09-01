from discord import Member
from discord.ext.commands import (
    BucketType,
    cooldown,
    Bot,
    Cog,
    command,
    Context
)
import time
from random import choice
from requests import get
from config.main import tenor_key
from json import loads
from config.embed import create_embed, gif_config


class FunCog(Cog, name="Fun Commands", description="Fun commands from your trusty Z Butler 💙"):

    def __init__(self, bot):
        self.bot = bot

    @command(name='SUS',
             usage="<username>",
             description="I think we got an imposter among us...",
             aliases=['sus', 'amogus', 'imposter'])
    async def SUS(self, ctx: Context, member: Member = None):
        """I think we got an imposter among us..."""
        if not member:
            member = ctx.message.author

        t = f".      　。　　　　•　    　  ﾟ　　    。"
        t2 = ".　　　.　　　  　　.　　　　　。　　     。　."
        t3 = ".　　      。　        ඞ   。　    .      •"
        t4 = f".      {member.mention} was The Imposter.　 。　."
        t5 = "　 　　。　　　　　　ﾟ　　　.　　　　　."
        t6 = ",         .　         .　　       ."

        final = f"{t2}\n{t3}\n{t4}\n{t5}\n{t6}"

        await ctx.send(final)

    @command(name="gif_search",
             usage="topic",
             description="Look for a gif about a certain topic",
             aliases=['gif?']
             )
    async def look_for_gif(self, ctx: Context, topic: str):
        """Look for a gif about a certain topic"""
        limit = 100

        r = get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" %
            (topic, tenor_key, limit))

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

    @command(
        name="ping",
        usage="",
        description="Show the bot's ping.")
    @cooldown(1, 2, BucketType.member)
    async def ping(self, ctx):
        """Show the bot's ping."""
        before = time.monotonic()

        message = await ctx.send("🏓 Pong !")

        ping = (time.monotonic() - before) * 1000

        await message.edit(content=f"🏓 Pong !  `{int(ping)} ms`")


def setup(bot: Bot):
    bot.add_cog(FunCog(Cog))
