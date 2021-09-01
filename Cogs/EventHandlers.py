from io import BytesIO

from discord.ext.commands.errors import CommandOnCooldown, MemberNotFound
from functions.create_welcome_image import create_picture
from discord import Member, Guild, File
from discord.abc import GuildChannel
from discord.ext.commands import Cog, Context


class EventHandlers(Cog, name="Event handlers", description="Events fired when somethings kicks in the server."):

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

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):

        if isinstance(error, MemberNotFound):
            await ctx.send('¯\\_(ツ)_/¯ The user provided could not be found, try again...')

        if isinstance(error, CommandOnCooldown):
            await ctx.send(f'⏳ Hold your horses, this command is on hold, you can use it in {round(error.retry_after, 2)} secs.')


def setup(bot):
    bot.add_cog(EventHandlers(bot))
