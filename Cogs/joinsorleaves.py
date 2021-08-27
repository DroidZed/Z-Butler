from discord import Member
from discord.ext.commands import Cog


class JoinsOrLeavesCog(Cog, name="joins or leaves commads"):

    def __init__(self, bot):
        self.bot = bot
        self.out_channel = 880824817555738655

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channel = member.guild.get_channel(self.out_channel)
        if channel is not None:
            await channel.send(f"<@{member.id}> has joined the server.")
        else:
            print('channel is none or missing perms')

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = member.guild.get_channel(self.out_channel)
        if channel is not None:
            await channel.send(f"<@{member.id}> has left the server.")
        else:
            print('channel is none or missing perms')


def setup(bot):
    bot.add_cog(JoinsOrLeavesCog(bot))
