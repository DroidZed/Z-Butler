from io import BytesIO
from sys import stderr
from traceback import print_exception
from typing import Optional

from discord import (
    File,
    Guild,
    Forbidden,
    TextChannel,
    Member,
    Role,
)
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
from modules.embedder.embedder_machine import (
    EmbedderMachine,
)

from modules.mongo.db_manager import MongoDBHelperClient
from config.colors import BOT_COLOR
from config.links import get_server_image
from config.main import GUILD_ID
from modules.welcome_image.create_welcome_image import (
    create_welcome_image,
)


class EventHandlers(
    Cog,
    name="Event Handlers",
    description="Events fired when something kicks in the server.",
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.out_channel = 1005545745291681873

    @staticmethod
    def __get_initial_roles(
        guild: Optional[Guild],
    ) -> list[Role]:
        lRoles = []

        if guild:
            lRoles.append(
                guild.get_role(1071798806275969086)
            )  # Lost Soul

        return lRoles

    @Cog.listener()
    async def on_member_join(self, member: Member):
        guild = self.bot.get_guild(GUILD_ID)

        channel = (
            guild.get_channel(self.out_channel)
            if guild
            else None
        )

        try:
            await member.add_roles(
                *self.__get_initial_roles(guild),
                reason="Starter roles",
                atomic=True,
            )
        except Forbidden as e:
            print(e)

        if channel and isinstance(channel, TextChannel):
            with BytesIO() as image_binary:
                create_welcome_image(
                    username=f"{member.name}",
                    discriminator=f"{member.discriminator}",
                ).save(image_binary, "PNG")

                image_binary.seek(0)

                try:
                    machine = EmbedderMachine()

                    machine.set_embed_components(
                        title=f"Hello there fellow Dragon Warrior",
                        description="Welcome to **DRAGON'S HEART** !! Please open a ticket in "
                        "<#778292937426731049> and a member of the staff team will be with you "
                        "shortly",
                    )

                    machine.add_footer(
                        footer_text="Your trusty bot Z 🔱",
                        footer_icon="https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    )

                    await member.send(embed=machine.embed)
                except Forbidden:
                    pass

                await channel.send(
                    content=f"👋🏻 <@{member.id}> a new recruit has joined the guild !! Bring the beer 🍻",
                    file=File(
                        fp=image_binary,
                        filename=f"{member.name}-welcome.png",
                    ),
                )

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        guild = self.bot.get_guild(GUILD_ID)

        channel = (
            guild.get_channel(self.out_channel)
            if guild
            else None
        )

        client = MongoDBHelperClient("users")

        if not (
            channel and isinstance(channel, TextChannel)
        ):
            return

        if await client.query_collection(
            {"uid": member.id}
        ):
            await client.delete_from_collection(
                {"uid": member.id}
            )

        machine = EmbedderMachine()

        machine.set_embed_components(
            title=f"{member.name} Left us.",
            description=f"<@{member.id}> got sucked into a black hole <a:black_hole:1071059323482021929>, long forgotten.",
            thumbnail_url=get_server_image(guild),
        )

        machine.add_footer(
            footer_icon="https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
            footer_text="We shall never remember those who left our cause.",
        )

        await channel.send(embed=machine.embed)

    @Cog.listener()
    async def on_command_error(
        self, ctx: Context, error: CommandError
    ):
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
                await ctx.send(
                    "Nope, no such command was found *sight* 💨",
                    mention_author=True,
                )

            case CommandInvokeError():
                await ctx.send(
                    "❌ Internal anomaly, I wasn't able to handle your request invoker. Sorry for my incompetence.",
                    mention_author=True,
                )
                print_exception(
                    type(error),
                    error,
                    error.__traceback__,
                    file=stderr,
                )

            case MissingRequiredArgument():
                await ctx.reply(
                    "You __***IDIOT***__ !! Don't you know when typing this command, YOU **MUST** provide "
                    "ARGUMENTS ? I think you should go back to elementary school and learn how to read 🙄",
                    mention_author=True,
                )

            case ReadTimeout():
                await ctx.reply(
                    "Command timed out, please try again ❌",
                    mention_author=True,
                )

            case _:
                print_exception(
                    type(error),
                    error,
                    error.__traceback__,
                    file=stderr,
                )


def setup(bot: Bot):
    bot.add_cog(EventHandlers(bot))
