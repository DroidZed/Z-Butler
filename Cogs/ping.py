from discord.ext.commands import (
    bot,
    BucketType,
    cooldown,
    Bot,
    Cog,
    command
)
import time


class PingCog(Cog, name="ping command"):
    def __init__(self, bot: bot):
        self.bot = bot

    @command(
        name="ping",
        usage="ping",
        description="Display the bot's ping.")
    @cooldown(1, 2, BucketType.member)
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("🏓 Pong !")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 Pong !  `{int(ping)} ms`")


def setup(bot: Bot):
    bot.add_cog(PingCog(bot))
