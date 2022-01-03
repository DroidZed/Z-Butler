from io import BytesIO
from sys import stderr
from traceback import print_exception

from discord import File, Guild
from discord.abc import GuildChannel
from discord.ext.commands import Bot, Cog, Context, MemberConverter
from discord.ext.commands.errors import (CommandError,
                                         CommandNotFound,
                                         CommandOnCooldown,
                                         MissingRole,
                                         CommandInvokeError, MemberNotFound, MissingRequiredArgument)
from httpx import ReadTimeout

from classes.MongoDBHelperClient import MongoDBHelperClient
from config.embed.leave import leave_config
from functions.create_welcome_image import create_picture
from functions.embed_factory import create_embed


class EventHandlers(Cog, name="Event Handlers", description="Events fired when something kicks in the server."):

    def __init__(self, bot):
        self.bot = bot
        self.out_channel = 696842023625424947

    @Cog.listener()
    async def on_member_join(self, member: MemberConverter):

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

    @Cog.listener()
    async def on_member_remove(self, member: MemberConverter):

        channel: GuildChannel = member.guild.get_channel(self.out_channel)

        client = MongoDBHelperClient("users")

        if not channel:
            return

        if client.query_collection({"uid": member.id}):
        
            client.delete_from_collection({
                "uid": member.id
            })

        await channel.send(embed=create_embed(leave_config(member.name, member.id)))

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):

        if isinstance(error, MemberNotFound):

            await ctx.reply('¯\\_(ツ)_/¯ The user provided could not be found, try again...')

        elif isinstance(error, CommandOnCooldown):

            await ctx.reply(
                f'⏳ Hold your horses, this command is on cooldown, you can use it in {round(error.retry_after, 2)}s')

        elif isinstance(error, CommandNotFound):

            await ctx.reply('Nope, no such command was found *sight* 💨')

        elif isinstance(error, CommandInvokeError):

            await ctx.reply(
                "Internal anomaly, I wasn't able to handle your request invoker. Sorry for my incompetence.")
            print_exception(type(error), error,
                            error.__traceback__, file=stderr)

        elif isinstance(error, MissingRequiredArgument):

            await ctx.reply("You __***IDIOT***__ !! Don't you know when typing this command, YOU **MUST** provide "
                            "ARGUMENTS ? I think you should go back to elementary school and learn how to read 🙄")

        elif isinstance(error, ReadTimeout):

            await ctx.reply("Command timed out, please try again ❌")

        else:
            if not isinstance(error, MissingRole):
                print_exception(type(error), error,
                                error.__traceback__, file=stderr)


def setup(bot: Bot):
    bot.add_cog(EventHandlers(bot))
