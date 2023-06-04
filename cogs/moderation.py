from discord import Role, Member
from discord.ext.commands import Bot, Cog, Context, command
from discord.ext.commands.core import has_guild_permissions
from discord.ext.commands.errors import CommandError, MissingPermissions

from classes.embed_factory import EmbedFactory
from modules.mongo.db_manager import MongoDBHelperClient
from config.embed.moderation_embeds import ban_config, kick_config, mute_config, unmute_config, no_perms_config, strike_config
from config.main import PREFIX


class ModerationCog(Cog, name="Moderation", description="🏛 Mod commands for **__Lord Lorkhan__** only."):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.db_client = MongoDBHelperClient("users")

    # ban kick warn purge mute & unmute

    @staticmethod
    async def __ban_user(ctx: Context, member: Member, reason: str, client: MongoDBHelperClient):

        async with ctx.typing():
            await client.delete_from_collection({"uid": member.id})

        await member.send(embed=EmbedFactory.create_embed(
            config=ban_config(),
            reason=reason or "3 Strikes",
            cfg_type="mod",
            Action="**BAN**",
        ))
        
        await ctx.send(f"User <@{member.id}> has been banned for {reason or '3 Strikes'} 🔨")
        await ctx.guild.ban(member, reason=reason or "3 Strikes")

    @staticmethod
    async def __strike_user(ctx: Context, member: Member, reason: str, strikes: int, client: MongoDBHelperClient):

        async with ctx.typing():
            await client.insert_into_collection([{"uid": member.id, "strike_count": 1, "reason": reason}])

        await member.send(
            embed=EmbedFactory.create_embed(
                config=strike_config(strikes),
                reason=reason or "Nothing",
                cfg_type="mod",
                Action="***STRIKE***",
            )
        )

        await ctx.send("The naughty user has been warned, hope he gets the message 😑")

    @staticmethod
    async def __strike_ban_user(ctx: Context, member: Member, reason: str, client: MongoDBHelperClient):

        user_query: list[dict] = await client.query_collection({"uid": member.id})

        user = user_query[0] if user_query else {}

        if not user_query:

            await ModerationCog.__strike_user(ctx, member, reason, 2, client)

        elif user["strike_count"] == 2:

            await ModerationCog.__ban_user(ctx, member, reason, client)

        else:

            async with ctx.typing():

                await client.update_document(
                    {"uid": user["uid"]},
                    {"$set": {"reason": reason}, "$inc": {"strike_count": 1}},
                )

                query = await client.query_collection({"uid": user["uid"]})

                nb_strikes = query[0]["strike_count"]

            await ModerationCog.__strike_user(ctx, member, reason, nb_strikes - 1, client)

    @staticmethod
    async def invalid_perms_embed(ctx: Context, action: str) -> None:
        await ctx.send(embed=EmbedFactory.create_embed(config=no_perms_config(), cfg_type=action))

    @staticmethod
    def __silenced_role(ctx: Context) -> Role:
        return ctx.guild.get_role(896349097391444029)

    @staticmethod
    def __dragon_warrior_role(ctx: Context) -> Role:
        return ctx.guild.get_role(969566082014785566)

    @command(
        name="ban",
        usage=f"{PREFIX}ban `username` `reason`",
        description="Ban a user for a specific reason.",
    )
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx: Context, member: Member, *reason: str):

        await self.__ban_user(ctx, member, " ".join(reason), self.db_client)

    @command(
        name="kick",
        usage=f"{PREFIX}kick `username` `reason`",
        description="Kick a user with a given reason.",
    )
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: Member, *reason: str):

        reason = " ".join(reason) if reason else "Nothing"

        msg = f"<@{member.id}> has been kicked for {reason} <a:kick:880995293179555852>"

        if not reason:
            msg = "Kicked without a reason, not that I care ¯\\_(ツ)_/¯"

        async with ctx.typing():
            await self.db_client.delete_from_collection({"uid": member.id})

        await ctx.guild.kick(member, reason=reason)

        await ctx.send(embed=EmbedFactory.create_embed(kick_config(msg), reason, None))

    @command(
        name="strike",
        usage=f"{PREFIX}strike `username` `reason`",
        description="Give a strike to a naughty user.",
    )
    @has_guild_permissions(kick_members=True)
    async def strike(self, ctx: Context, member: Member, *reason: str):

        await self.__strike_ban_user(ctx, member, " ".join(reason), self.db_client)

    @command(
        name="purge",
        usage=f"{PREFIX}purge `amount`",
        description="Clears a certain amount of messages, can't delete those older than 14 days though.",
    )
    @has_guild_permissions(manage_messages=True)
    async def purge(self, ctx: Context, amount: int):
        await ctx.channel.purge(limit=amount)

    @command(name="mute", usage=f"{PREFIX}mute `username`", description="Mutes a member.")
    @has_guild_permissions(kick_members=True)
    async def mute(self, ctx: Context, member: Member):

        if self.__silenced_role(ctx) in member.roles:
            await ctx.message.reply("User already muted you dumb fuck !", mention_author=True)
            return

        await ctx.message.delete()

        await member.remove_roles(self.__dragon_warrior_role(ctx))

        await member.add_roles(self.__silenced_role(ctx))

        await ctx.send(embed=EmbedFactory.create_embed(mute_config(member.id)))

    @command(name="!mute", usage=f"{PREFIX}!mute `username`", description="UNmutes a muted member.")
    @has_guild_permissions(kick_members=True)
    async def unmute(self, ctx: Context, member: Member):

        if self.__silenced_role(ctx) not in member.roles:
            await ctx.message.reply("User already unmuted...what a waste of time 🙄", mention_author=True)
            return

        await ctx.message.delete()

        await member.remove_roles(self.__silenced_role(ctx))

        await member.add_roles(self.__dragon_warrior_role(ctx))

        await ctx.send(embed=EmbedFactory.create_embed(unmute_config(member.id)))

    # error handlers

    @purge.error
    async def purge_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "purge")

    @ban.error
    async def ban_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "ban")

    @kick.error
    async def kick_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "kick")

    @strike.error
    async def strike_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "strike")

    @mute.error
    async def mute_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "mute")

    @unmute.error
    async def unmute_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            await self.invalid_perms_embed(ctx, "unmute")


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
