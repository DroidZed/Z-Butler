from io import BytesIO
from sys import stderr
from traceback import print_exception

from discord import File, Guild, Member
from discord.abc import GuildChannel
from discord.ext.commands import Cog, Context
from discord.ext.commands.errors import (CommandError, CommandNotFound,
                                         CommandOnCooldown, MemberNotFound)
from functions.create_welcome_image import create_picture
from httpx import ReadTimeout
from tinydb import Query, TinyDB

users = TinyDB('database/db.json').table("users")
UsersQuery = Query()


class EventHandlers(Cog, name="Event Handlers", description="Events fired when somethings kicks in the server."):

    def __init__(self, bot):
        self.bot = bot
        self.out_channel = 696842023625424947

    @Cog.listener()
    async def on_member_join(self, member: Member):

        guild: Guild = member.guild

        channel: GuildChannel = guild.get_channel(self.out_channel)

        if channel:

            with BytesIO() as image_binary:

                create_picture(username=f'{member.name}',
                               discriminator=f'{member.discriminator}').save(image_binary, 'PNG')

                image_binary.seek(0)

                await channel.send(
                    content=f"👋🏻 <@{member.id}> finally landed on Dragon's Heart !! Bring the beer 🍻",
                    file=File(
                        fp=image_binary,
                        filename=f'{member.name}-welcome.png'
                    )
                )
        else:

            print('channel is none or missing perms')

    @Cog.listener()
    async def on_member_remove(self, member: Member):

        channel = member.guild.get_channel(self.out_channel)

        if channel:

            if users.contains((UsersQuery.id == member.id)):

                users.remove(UsersQuery.id == member.id)

            await channel.send(content=f"<@{member.id}> has been mercylessly thrown into Oblivion ⚰, long forgotten.")

        else:

            print('channel is none or missing perms')

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):

        if isinstance(error, MemberNotFound):
            await ctx.send('¯\\_(ツ)_/¯ The user provided could not be found, try again...')

        elif isinstance(error, CommandOnCooldown):
            await ctx.send(f'⏳ Hold your horses, this command is on hold, you can use it in {round(error.retry_after, 2)} secs.')

        elif isinstance(error, CommandNotFound):
            await ctx.send('Nope, no such command was found *sight* 💨')

        elif isinstance(error, ReadTimeout):
            await ctx.send("Command timed out, please try again ❌")

        else:
            print_exception(
                type(error), error, error.__traceback__, file=stderr)


def setup(bot):
    bot.add_cog(EventHandlers(bot))
