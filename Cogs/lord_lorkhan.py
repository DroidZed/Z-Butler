from discord.ext.commands import Bot, BucketType, Cog, Context, command, cooldown, has_role

from classes.tweepy_wrapper import TweepyWrapper
from classes.tweet_model import TweetModel
from config.embed.tweet import tweet_config
from config.main import PREFIX, CROWN_ROLE_ID
from functions.embed_factory import create_embed


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

        await ctx.send(embed=create_embed(tweet_config(result.text, result.t_id, "Droid7ed")))

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

        await ctx.send(embed=create_embed(tweet_config(result.text, result.t_id, "Droid7ed")))


def setup(bot: Bot):
    bot.add_cog(LorkhanCommands(bot))
