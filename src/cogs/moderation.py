from discord import Member
from discord.ext.commands import Bot, Cog, Context, command
from discord.ext.commands.core import has_guild_permissions
from discord.ext.commands.errors import (
    CommandError,
    MissingPermissions,
)

from modules.embedder import ZembedField, generate_embed
from modules.mongo.db_manager import MongoDBHelperClient
from utils import Env


class ModerationCog(
    Cog,
    name="Moderation",
    description="🏛 Mod commands for **__Lord Lorkhan__** only.",
):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.db_client = MongoDBHelperClient("users")

    # ban kick warn purge mute & unmute

    @staticmethod
    async def __ban_user(
        ctx: Context,
        member: Member,
        reason: str,
        client: MongoDBHelperClient,
    ):
        async with ctx.typing():
            await client.delete_from_collection({"uid": member.id})

        fields = [
            ZembedField(
                name="Reason",
                value=reason or "3 Strikes",
                inline=True,
            ),
            ZembedField(name="Action", value="**BAN**", inline=True),
        ]

        embed = generate_embed(
            title="YOU HAVE BEEN BANNED",
            url="https://media1.tenor.com/images/0dcb84c900e10b6272152cd759eb1eab/tenor.gif",
            description="After the actions you've done in my server the admin decided to ban you for the safety of our "
            "community.",
            color=Env.CROWN_COLOR,
            image_url="https://media1.tenor.com/images/0dcb84c900e10b6272152cd759eb1eab/tenor.gif",
            footer_icon="https://emoji.gg/assets/emoji/3886_BAN.gif",
            footer_text="Next time think twice before making trouble in a server 😶",
            *fields,
        )

        await member.send(embed=embed)

        await ctx.send(
            f"User <@{member.id}> has been banned for {reason or '3 Strikes'} 🔨"
        )
        if ctx.guild:
            await ctx.guild.ban(member, reason=reason or "3 Strikes")

    @staticmethod
    async def __strike_user(
        ctx: Context,
        member: Member,
        reason: str,
        strikes: int,
        client: MongoDBHelperClient,
    ):
        async with ctx.typing():
            await client.insert_into_collection(
                [
                    {
                        "uid": member.id,
                        "strike_count": 1,
                        "reason": reason,
                    }
                ]
            )

        fields = [
            ZembedField(
                name="Reason",
                value=reason or "No reason at all!",
                inline=True,
            ),
            ZembedField(
                name="Action",
                value="***STRIKE***",
                inline=True,
            ),
        ]

        embed = generate_embed(
            title="YOU GOT A STRIKE, MIND YOUR OWN BUSINESS NEXT TIME.",
            url="https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
            description="HOLD UP THERE ! BAD THINGS ARE NOT ALLOWED HERE, DO IT ELSEWHERE OR FACE THE CONSEQUENCES !",
            color=Env.CROWN_COLOR,
            image_url="https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
            footer_text=f"{strikes} Strikes and you're banned.",
            footer_icon="https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif?1542340473",
            *fields,
        )

        await member.send(embed=embed)

        await ctx.send(
            "The naughty user has been warned, hope he gets the message 😑"
        )

    @staticmethod
    async def __strike_ban_user(
        ctx: Context,
        member: Member,
        reason: str,
        client: MongoDBHelperClient,
    ):
        user_query = await client.query_collection({"uid": member.id})

        nb_strikes = 0

        user = user_query[0] if user_query else {}

        if not user_query:
            await ModerationCog.__strike_user(ctx, member, reason, 2, client)

        elif user["strike_count"] == 2:
            await ModerationCog.__ban_user(ctx, member, reason, client)

        else:
            async with ctx.typing():
                await client.update_document(
                    {"uid": user["uid"]},
                    {
                        "$set": {"reason": reason},
                        "$inc": {"strike_count": 1},
                    },
                )

                query = await client.query_collection({"uid": user["uid"]})

                if not query:
                    return await ctx.send("Couldn't find the user!")

                else:
                    nb_strikes = query[0]["strike_count"]

            await ModerationCog.__strike_user(
                ctx, member, reason, nb_strikes - 1, client
            )

    @staticmethod
    async def invalid_perms_embed(ctx: Context, action: str) -> None:
        def resolve_footer():
            return {
                "ban": {
                    "text": "How funny...the admin should see this 😶",
                    "icon_url": "https://emoji.gg/assets/emoji/3886_BAN.gif",
                },
                "strike": {
                    "text": "Next time make sure you have enough permissions, what a shame 🤐",
                    "icon_url": "https://emojis.slackmojis.com/emojis/images/1542340473/4982/watching-you.gif",
                },
                "kick": {
                    "text": "You are not cool enough for this 🥱",
                    "icon_url": "https://emojis.slackmojis.com/emojis/images/1620894162/38676/kicking.gif",
                },
                "purge": {
                    "text": "Cleaning behind you mess ? What a dog...🤮",
                    "icon_url": "https://emojis.slackmojis.com/emojis/images/1472329131/1120/nuclear-bomb.gif",
                },
                "mute": {
                    "text": "Shushing your own kin ? You dumb bro ?",
                    "icon_url": "https://c.tenor.com/_g7PgSa_6vIAAAAS/speechless-mute.gif",
                },
                "unmute": {
                    "text": "The silenced shall remain unheard of, buried under the misery of their own mistakes.",
                    "icon_url": "https://c.tenor.com/lXqsq1j6KTUAAAAS/matrix-mouth.gif",
                },
            }

        embed = generate_embed(
            title="You SUSSY BAKA !",
            url="https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
            description="You're not powerful enough to use this command, how pitiful 😒",
            color=Env.BOT_COLOR,
            image_url="https://c.tenor.com/ep6ztNAdFMcAAAAC/hank-schrider-sussy-baka.gif",
            footer_text=resolve_footer()[action]["text"],
            footer_icon=resolve_footer()[action]["icon_url"],
        )

        await ctx.send(embed=embed)

    @staticmethod
    def __silenced_role(ctx: Context):
        return ctx.guild.get_role(896349097391444029) if ctx.guild else None

    @staticmethod
    def __server_default_role(ctx: Context):
        return ctx.guild.get_role(1065632523507478598) if ctx.guild else None

    @command(
        name="ban",
        usage=f"{Env.PREFIX}ban `username` `reason`",
        description="Ban a user for a specific reason.",
    )
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx: Context, member: Member, *reason: str):
        await self.__ban_user(ctx, member, " ".join(reason), self.db_client)

    @command(
        name="kick",
        usage=f"{Env.PREFIX}kick `username` `reason`",
        description="Kick a user with a given reason.",
    )
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: Member, *reason: str):
        res = " ".join(reason) if reason else "Nothing"

        msg = f"<@{member.id}> has been kicked for {reason} <a:kick:880995293179555852>"

        if not reason:
            msg = "Kicked without a reason, not that I care ¯\\_(ツ)_/¯"

        async with ctx.typing():
            await self.db_client.delete_from_collection({"uid": member.id})

        if ctx.guild:
            await ctx.guild.kick(member, reason=res)

            embed = generate_embed(
                description=msg,
                color=Env.CROWN_COLOR,
                *[ZembedField("Reason", reason, False)],
            )

            await ctx.send(embed=embed)

    @command(
        name="strike",
        usage=f"{Env.PREFIX}strike `username` `reason`",
        description="Give a strike to a naughty user.",
    )
    @has_guild_permissions(kick_members=True)
    async def strike(self, ctx: Context, member: Member, *reason: str):
        await self.__strike_ban_user(
            ctx, member, " ".join(reason), self.db_client
        )

    @command(
        name="purge",
        usage=f"{Env.PREFIX}purge `amount`",
        description="Clears a certain amount of messages, can't delete those older than 14 days though.",
    )
    @has_guild_permissions(manage_messages=True)
    async def purge(self, ctx: Context, amount: int):
        await ctx.channel.purge(limit=amount)  # type: ignore

    @command(
        name="mute",
        usage=f"{Env.PREFIX}mute `username`",
        description="Mutes a member.",
    )
    @has_guild_permissions(kick_members=True)
    async def mute(self, ctx: Context, member: Member):
        silenced_role = self.__silenced_role(ctx)
        default_role = self.__server_default_role(ctx)

        if not silenced_role:
            return await ctx.send("❌ Invaid role!")

        else:
            if silenced_role in member.roles:
                await ctx.message.reply(
                    "User already muted you dumb fuck !",
                    mention_author=True,
                )
                return

            await ctx.message.delete()

            if default_role:
                await member.remove_roles(default_role)

            await member.add_roles(silenced_role)

            embed = generate_embed(
                title="The hammer has fallen",
                color=Env.BOT_COLOR,
                description=f"Silenced <@{member.id}>. Take the time to seek help.",
                footer_text="Dragon's Heart Team.",
                footer_icon=Env.SERVER_IMAGE,
            )

            await ctx.send(embed=embed)

    @command(
        name="!mute",
        usage=f"{Env.PREFIX}!mute `username`",
        description="UNmutes a muted member.",
    )
    @has_guild_permissions(kick_members=True)
    async def unmute(self, ctx: Context, member: Member):
        silenced_role = self.__silenced_role(ctx)
        default_role = self.__server_default_role(ctx)

        if silenced_role not in member.roles:
            await ctx.message.reply(
                "User already unmuted...what a waste of time 🙄",
                mention_author=True,
            )
            return

        await ctx.message.delete()

        await member.remove_roles(silenced_role)

        if default_role:
            await member.add_roles(default_role)

        embed = generate_embed(
            title="Forgiveness is a choice",
            color=Env.BOT_COLOR,
            description=f"Unmuted <@{member.id}>. Hopefully you've reflected on your actions.",
            footer_text="Dragon's Heart Team.",
            footer_icon=Env.SERVER_IMAGE,
        )

        await ctx.send(embed=embed)

    # error handlers

    @purge.error  # type: ignore
    async def purge_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "purge")

    @ban.error  # type: ignore
    async def ban_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "ban")

    @kick.error  # type: ignore
    async def kick_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "kick")

    @strike.error  # type: ignore
    async def strike_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "strike")

    @mute.error  # type: ignore
    async def mute_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "mute")

    @unmute.error  # type: ignore
    async def unmute_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "unmute")


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
