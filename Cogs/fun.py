import time
from asyncio import sleep
from random import randint as rdn

from config.embed.eight_ball import eight_ball_config
from config.embed.gif import gif_config
from config.embed.how_gay import how_gay_config
from config.embed.ping import ping_config
from config.main import PREFIX
from discord import Message
from discord.ext.commands import (Bot, BucketType, Cog, Context,
                                  MemberConverter, command, cooldown)
from functions.eight_ball_api import eight_ball_api
from functions.embed_factory import create_embed
from functions.find_gif import find_gif
from functions.gay_commentary import gay_commentary
from httpx import ReadTimeout


class FunCog(
        Cog,
        name="Fun Commands",
        description="Fun commands from your trusty Z Butler 💙"):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='SUS',
             usage=f"{PREFIX}SUS `username`",
             description="I think we got an imposter among us...",
             aliases=['sus', 'amogus', 'imposter'])
    @cooldown(1, 5, BucketType.user)
    async def sus(self, ctx: Context, member: MemberConverter = None) -> None:
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
             usage=f"{PREFIX}gif_search `query`",
             description="Look for a gif about a certain topic",
             aliases=['gif?']
             )
    @cooldown(1, 15, BucketType.user)
    async def look_for_gif(self, ctx: Context, *query: str) -> None:

        topic = " ".join(query)
        async with ctx.typing():
            result_set = await find_gif(topic)

        if result_set:
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
    async def ping(self, ctx: Context) -> None:

        await ctx.message.delete()

        start_time = time.time()
        message: Message = await ctx.send(embed=create_embed(ping_config("🏓 Pong !")))
        end_time = time.time()

        fields = {
            'API': f'`{round((end_time - start_time) * 1000)}ms`',

            'Bot Latency': f'`{round(self.bot.latency * 1000)}ms`'

        }

        await message.edit(embed=create_embed(ping_config("🏓 Pong!"), None, 'ping', **fields))

    @command(
        name="howgay",
        usage=f"{PREFIX}howgay `username`",
        description="Checks how gay a user is, ew...",
        aliases=['hg'])
    async def how_gay(self, ctx: Context, member: MemberConverter = None) -> None:

        if member is None:
            member = ctx.author

        rate = rdn(0, 100)

        msg = gay_commentary(rate)

        config = how_gay_config(username=member.name,
                                mention=member.mention,
                                rate=rate,
                                msg=msg)

        if rate > 65:
            config.update({"image": {
                          'url': "https://c.tenor.com/GTjxHh4xr2kAAAAC/you-are-an-abomination-creature.gif"}})

        embed = create_embed(config=config)

        await ctx.send(embed=embed)

    @command(
        name="8ball",
        usage=f"{PREFIX}8ball `question`",
        description="Ask the magical 8 ball about anything.",
        aliases=['8b'])
    @cooldown(1, 5, BucketType.member)
    async def _8_ball(self, ctx: Context, *question: str) -> None:

        if not question:
            await ctx.send("No question provided 🙄")
        else:
            try:
                qst = " ".join(question)
                async with ctx.typing():
                    api_resp = await eight_ball_api(qst)
                if api_resp:

                    if api_resp['success']:

                        config = gif_config(
                            "https://media.tenor.com/images/67155da2720fa29220200465f1a4bd84/tenor.gif",
                            "Z Butler",
                            "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                            "8-Ball Game",
                            "https://tenor.com/view/skeleton-eightball-8ball-prediction-horoscope-gif-13531133"
                        )

                        config["description"] = "Thinking..."

                        await ctx.send(embed=create_embed(config), delete_after=5)

                        await sleep(5)

                        await ctx.send(embed=create_embed(
                            eight_ball_config(
                                ctx.message.author.mention, api_resp['body']['answer']),
                            None,
                            None)
                        )
                else:
                    await ctx.send("I wasn't succesful at determining an answer.")
                    return

            except ReadTimeout:
                await ctx.send("Command timed out, please try again ❌")
                return


def setup(bot: Bot):
    bot.add_cog(FunCog(bot))
