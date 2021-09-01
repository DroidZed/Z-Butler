from io import BytesIO
from functions.create_welcome_image import create_picture
from discord import Member, Guild, File
from discord.abc import GuildChannel
from discord.ext.commands import Cog


class JoinsOrLeavesCog(Cog, name="Join / Leave Events", description="Events fired when a user joins or leaves the server."):

    def __init__(self, bot):
        self.bot = bot
        self.out_channel = 696842023625424947

    @Cog.listener()
    async def on_member_join(self, member: Member):

        guild: Guild = member.guild

        channel: GuildChannel = guild.get_channel(self.out_channel)

        if channel is not None:

            with BytesIO() as image_binary:

                create_picture(username=f'{member.name}',
                               discriminator=f'{member.discriminator}').save(image_binary, 'PNG')

                image_binary.seek(0)

                await channel.send(content=f"👋🏻 <@{member.id}> finally landed on Dragon's Heart !! Bring the beer 🍻",
                                   file=File(fp=image_binary, filename=f'{member.name}-welcome.png'))
        else:
            print('channel is none or missing perms')

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = member.guild.get_channel(self.out_channel)
        if channel is not None:
            await channel.send(content=f"<@{member.id}> has been mercylessly thrown into Oblivion ⚰, long forgotten.")
        else:
            print('channel is none or missing perms')


def setup(bot):
    bot.add_cog(JoinsOrLeavesCog(bot))
