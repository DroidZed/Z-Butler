from discord.ext.commands import Bot, BucketType, Cog, Context, command, cooldown, has_role

from classes.embed_factory import EmbedFactory
from classes.twitter_ import TweepyWrapper
from classes.twitter_ import TweetModel
from config.colors import TWITTER_COLOR
from config.links import server_image
from config.main import PREFIX, CROWN_ROLE_ID


class LorkhanCommands(
    Cog,
    name="Admin category",
    description="[ADMIN ONLY]",
):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="tweet",
        description="Sends a tweet. Will fail if the tweet is too long (> 280 characters)",
        usage=f"{PREFIX}tweet `message`",
    )
    @cooldown(1, 2.5, BucketType.user)
    @has_role(CROWN_ROLE_ID)
    async def tweet(self, ctx: Context, *message: str):

        async with ctx.typing():
            result: TweetModel = await TweepyWrapper().tweet(text=" ".join(_ for _ in message))

        if result.err:
            await ctx.send(
                "Your tweet is too long ! Please use the reply function to create a thread with shorter tweets !"
            )
            return

        await self.__send_tweet(ctx, result)

    @command(
        name="reply",
        description="Sends a reply to a tweet. Will fail if the reply is too long (> 280 characters)",
        usage=f"{PREFIX}reply `tweet_id` `message`",
    )
    @cooldown(1, 2.5, BucketType.user)
    @has_role(CROWN_ROLE_ID)
    async def reply(self, ctx: Context, t_id: int, *message: str):

        async with ctx.typing():

            result: TweetModel = await TweepyWrapper().tweet(
                text=" ".join(_ for _ in message), reply=True, tweet_id=t_id
            )

        if t_id <= 0 or not t_id:
            await ctx.reply("Please provide a valid tweet id !", mention_author=True)
            return

        if result.err:
            await ctx.reply(
                "Your tweet is too long ! Please use the reply function to create a thread with shorter tweets !",
                mention_author=True,
            )
            return

        await self.__send_tweet(ctx, result)

    @staticmethod
    async def __send_tweet(ctx, result):
        await ctx.send(
            embed=EmbedFactory.create_embed(
                EmbedFactory.create_config(
                    title="The bird tweets",
                    url=f"https://twitter.com/DroidZed/status/{result.t_id}",
                    color=TWITTER_COLOR,
                    description=f"`{result.text}`",
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={
                        "url": server_image
                    },
                    footer={
                        "text": f"Tweeted by Droid7ed - id: {result.t_id}",
                        "icon_url": "https://www.brandcolorcode.com/media/twitter-logo.png",
                    },
                )
            )
        )


def setup(bot: Bot):
    bot.add_cog(LorkhanCommands(bot))
