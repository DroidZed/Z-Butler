from io import BytesIO
from sys import stderr
from traceback import print_exception
from typing import Optional

from discord import File, Guild, Role, Forbidden, TextChannel, Member
from discord.ext.commands import Bot, Cog, Context
from discord.ext.commands.errors import (
    CommandError,
    MemberNotFound,
    CommandNotFound,
    CommandOnCooldown,
    MissingPermissions,
    CommandInvokeError,
    MissingRequiredArgument,
)

from httpx import ReadTimeout

from classes.embed_factory import EmbedFactory
from classes.mongo_db_management import MongoDBHelperClient
from config.colors import BOT_COLOR
from config.links import server_image
from config.main import GUILD_ID
from functions.image_manipulation import create_welcome_picture


class EventHandlers(
    Cog,
    name="Event Handlers",
    description="Events fired when something kicks in the server.",
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.out_channel = 696842023625424947

    @staticmethod
    def __get_initial_roles(guild: Optional[Guild]):

        return (
            [
                guild.get_role(896349097391444029),  # silenced role
                guild.get_role(980527744062464030),  # special roles
                guild.get_role(898874934615482378),  # default Seperator role 1
                guild.get_role(983415194967490641),  # default Seperator role 2
                guild.get_role(898874121222516736),  # community roles
                guild.get_role(969706983777263677),  # gaming roles
                guild.get_role(969639120513163345),  # newspaper roles
            ]
            if guild
            else []
        )

    @Cog.listener()
    async def on_member_join(self, member: Member):

        guild = self.bot.get_guild(GUILD_ID)

        channel: TextChannel | None = guild.get_channel(self.out_channel) if guild != None else None

        try:
            await member.add_roles(self.__get_initial_roles(guild), reason = "Starter roles", atomic = True)
        except Forbidden as e:
            print(f"error in role: {e!repr}")

        if channel:
            with BytesIO() as image_binary:
                create_welcome_picture(username=f"{member.name}", discriminator=f"{member.discriminator}").save(
                    image_binary, "PNG"
                )

                image_binary.seek(0)

                try:
                    await member.send(
                        embed=EmbedFactory.create_embed(
                            EmbedFactory.create_config(
                                title=f"Hello there fellow Dragon Warrior",
                                color=BOT_COLOR,
                                description="Welcome to **DRAGON'S HEART** !! Please open a ticket in "
                                "<#778292937426731049> and a member of the staff team will be with you "
                                "shortly",
                                author={
                                    "name": "The Z Butler",
                                    "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586"
                                    "/bb7df4730c048faacd8db6dd99291cdb.jpg",
                                },
                                thumbnail={"url": server_image},
                                footer={
                                    "text": "Your trusty bot Z 🔱",
                                    "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586"
                                    "/bb7df4730c048faacd8db6dd99291cdb.jpg",
                                },
                            )
                        )
                    )
                except Forbidden:
                    pass

                await channel.send(
                    content=f"👋🏻 <@{member.id}> a new recruit has joined the guild !! Bring the beer 🍻",
                    file=File(fp=image_binary, filename=f"{member.name}-welcome.png"),
                )

    @Cog.listener()
    async def on_member_remove(self, member: Member):

        channel: TextChannel = self.bot.get_guild(GUILD_ID).get_channel(self.out_channel)

        client = MongoDBHelperClient("users")

        if not channel:
            return

        if await client.query_collection({"uid": member.id}):
            await client.delete_from_collection({"uid": member.id})

        await channel.send(
            embed=EmbedFactory.create_embed(
                EmbedFactory.create_config(
                    title=f"{member.name} Left us.",
                    color=BOT_COLOR,
                    description=f"<@{member.id}> "
                    "got sucked into a black hole <a:black_hole:796434656605765632>, long forgotten.",
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586"
                        "/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={"url": server_image},
                    footer={
                        "text": "We shall never remember those who left our cause.",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586"
                        "/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                )
            )
        )

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):

        match error:

            case MissingPermissions():
                return

            case MemberNotFound():
                await ctx.reply(
                    "¯\\_(ツ)_/¯ The user provided could not be found, try again...",
                    mention_author=True,
                )

            case CommandOnCooldown():

                await ctx.reply(
                    f"⏳ Hold your horses, this command is on cooldown, you can use it in {round(error.retry_after, 2)}s",
                    mention_author=True,
                )

            case CommandNotFound():

                await ctx.send("Nope, no such command was found *sight* 💨", mention_author=True)

            case CommandInvokeError():

                await ctx.send(
                    "❌ Internal anomaly, I wasn't able to handle your request invoker. Sorry for my incompetence.",
                    mention_author=True,
                )
                print_exception(type(error), error, error.__traceback__, file=stderr)

            case MissingRequiredArgument():

                await ctx.reply(
                    "You __***IDIOT***__ !! Don't you know when typing this command, YOU **MUST** provide "
                    "ARGUMENTS ? I think you should go back to elementary school and learn how to read 🙄",
                    mention_author=True,
                )

            case ReadTimeout():

                await ctx.reply("Command timed out, please try again ❌", mention_author=True)

            case _:
                print_exception(type(error), error, error.__traceback__, file=stderr)


def setup(bot: Bot):
    bot.add_cog(EventHandlers(bot))
