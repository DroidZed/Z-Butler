from random import choice

from discord.ext.commands import (Bot,
                                  Cog,
                                  Context,
                                  command,
                                  cooldown,
                                  BucketType)

from config.embed.env_cfg import env_config
from config.main import PREFIX, OWNER_ID
from functions.embed_factory import create_embed


class ZedCog(Cog, name="Zed-Domain", description="⚡ Domain expansion !"):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="Z",
        description="Calls the bot.",
        usage=f"{PREFIX}",
        aliases=[""]
    )
    @cooldown(1, 2.5, BucketType.user)
    async def zed(self, ctx: Context):
        replies = [
            "WHAT ?!",
            "What do you need ?",
            "I'm busy attending to the __server, move along...",
            "Don't bother me you stupid !",
            "Go out there and touch some grass !!",
            "Shouldn't you be outside finding a partner instead ? You miserable virgin !!",
            "I bet your parents aren't proud of you and your gf/bf things you're a boring little clamp !"
        ]

        if ctx.author.id == OWNER_ID:
            await ctx.message.reply("Hello master 😍", mention_author=True)
            return

        await ctx.message.reply(choice(replies), mention_author=True)

    @command(
        name="env",
        description="Displays the bot's environment",
        usage=f"{PREFIX}env"
    )
    async def env(self, ctx: Context):
        await ctx.send(embed=create_embed(env_config(), None, None))


def setup(bot: Bot):
    bot.add_cog(ZedCog(bot))
