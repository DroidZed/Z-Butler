from discord import Member
from discord.ext.commands import Cog, bot

# TODO: Make this work.


class JoinsOrLeavesCog(Cog, name="joins or leaves commads"):

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channel = member.guild.get_channel(696842023625424947)
        if channel is not None:
            await channel.send("User has joined the server.")

    @Cog.listener()
    async def on_member_leave(self, member):
        channel = member.guild.get_channel(696842023625424947)
        if channel is not None:
            await channel.send("User has left the server.")


def setup(bot: bot):
    bot.add_cog(JoinsOrLeavesCog(bot))
