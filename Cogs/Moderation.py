from discord import Role
from discord.ext.commands import Bot, Cog, Context, MemberConverter, command
from discord.ext.commands.core import has_role
from discord.ext.commands.errors import CommandError, MissingRole

from classes.MongoDBHelperClient import MongoDBHelperClient
from config.embed.ban import ban_config
from config.embed.kick import kick_config
from config.embed.no_perms import no_perms_config
from config.embed.strike import strike_config
from config.main import CROWN_ROLE_ID, PREFIX
from functions.embed_factory import create_embed


async def _ban_user(ctx: Context, member: MemberConverter, reason: str):
    client = MongoDBHelperClient()

    async with ctx.typing():
        client.delete_from_collection("users", {
            "uid": member.id
        })

    await member.send(
        embed=create_embed(
            config=ban_config,
            reason=reason or "3 Strikes",
            cfg_type='mod',
            Action='**BAN**'
        )
    )
    await ctx.send(f"User <@{member.id}> has been banned for {reason or '3 Strikes'} 🔨")
    await ctx.guild.ban(member, reason=reason or '3 Strikes')


async def _strike_user(ctx: Context, member: MemberConverter, reason: str, strikes: int):
    await member.send(
        embed=create_embed(
            config=strike_config(strikes),
            reason=reason or "Nothing",
            cfg_type='mod',
            Action='***STRIKE***',
        )
    )

    await ctx.send("The naughty user has been warned, hope he gets the message 😑")


async def _strike_ban_user(ctx: Context, member: MemberConverter, reason: str):
    client = MongoDBHelperClient()

    user_query: list[dict] = client.query_collection("users", {
        "uid": member.id
    })

    user = user_query[0] if user_query else {}

    if not user_query:

        async with ctx.typing():

            client.insert_into_collection("users", [{'uid': member.id, 'strike_count': 1, "reason": reason}])

        await _strike_user(ctx, member, reason, 2)

    elif user["strike_count"] == 2:

        await _ban_user(ctx, member, reason)

    else:

        async with ctx.typing():

            client.update_document("users", {"uid": user["uid"]}, {
                "$set":
                    {
                        "reason": reason
                    },
                "$inc":
                    {
                        "strike_count": 1
                    }
            })

            nb_strikes = client.query_collection("users", {"uid": user["uid"]})[0]['strike_count']

        await _strike_user(ctx,
                           member,
                           reason,
                           nb_strikes - 1)


async def invalid_perms_embed(ctx: Context, action: str) -> None:
    await ctx.send(
        embed=create_embed(
            config=no_perms_config(),
            cfg_type=action
        )
    )


def silenced_role(ctx: Context) -> Role:
    return ctx.guild.get_role(896349097391444029)


class ModerationCog(Cog, name="Moderation", description="🏛 Mod commands for **__Lord Lorkhan__** only."):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    # ban kick warn purge mute & unmute

    @command(
        name="ban",
        usage=f"{PREFIX}ban `username` `reason`",
        description="Ban a user for a specific reason.")
    @has_role(CROWN_ROLE_ID)
    async def ban(self, ctx: Context, member: MemberConverter = None, *reason: str):

        if not member or member == ctx.message.author:
            await ctx.channel.send("No user provided 🙄 / You cannot ban yourself ⚓")
            return

        await _ban_user(ctx, member, ' '.join(reason))

    @command(
        name="kick",
        usage=f"{PREFIX}kick `username` `reason`",
        description="Kick a user with a given reason.")
    @has_role(CROWN_ROLE_ID)
    async def kick(self, ctx: Context, member: MemberConverter = None, *reason: str):

        if not member or member == ctx.message.author:
            await ctx.channel.send(embed=create_embed(kick_config("You cannot kick yourself ⚓ you stupid...")))
            return

        rs = " ".join(reason) if reason else 'Nothing'

        msg = f"<@{member.id}> has been kicked for {rs} <a:kick:880995293179555852>"

        if not reason:
            msg = "Kicked without a reason, not that I care ¯\\_(ツ)_/¯"

        async with ctx.typing():
            client = MongoDBHelperClient()

            client.delete_from_collection("users", {
                "uid": member.id
            })

        await ctx.guild.kick(member, reason=rs)

        await ctx.send(embed=create_embed(kick_config(msg), rs, None))

    @command(
        name="strike",
        usage=f"{PREFIX}strike `username` `reason`",
        description="Give a strike to a naughty user.")
    @has_role(CROWN_ROLE_ID)
    async def strike(self, ctx: Context, member: MemberConverter = None, *reason: str):

        if not member or member == ctx.message.author:
            await ctx.channel.send("Why would you strike yourself 🙄 ?")
            return

        await _strike_ban_user(ctx, member, ' '.join(reason))

    @command(
        name="purge",
        usage=f"{PREFIX}purge `amount`",
        description="Clears a certain amount of messages, can't delete those older than 14 days though.")
    @has_role(CROWN_ROLE_ID)
    async def purge(self, ctx: Context, amount: int):
        await ctx.channel.purge(limit=amount)

    @command(
        name="mute",
        usage=f"{PREFIX}mute `username`",
        description="Mutes a member.")
    @has_role(CROWN_ROLE_ID)
    async def mute(self, ctx: Context, member: MemberConverter):

        if member.top_role == silenced_role(ctx):
            await ctx.message.reply("User already muted you dump fuck !")
            return

        await member.add_roles(silenced_role(ctx))
        await ctx.send(f":white_check_mark: Muted {member.mention}. Take the time to seek help.")

    @command(
        name="!mute",
        usage=f"{PREFIX}!mute `username`",
        description="UNmutes a muted member.")
    @has_role(CROWN_ROLE_ID)
    async def unmute(self, ctx: Context, member: MemberConverter):

        if member.top_role != silenced_role(ctx):
            await ctx.message.reply("User already unmuted...what a waste of time 🙄")
            return

        await member.remove_roles(silenced_role(ctx))

        await ctx.send(f":white_check_mark: {member.mention} was unmuted. Hopefully you've reflected on your actions.")

    # error handlers

    @purge.error
    async def purge_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await invalid_perms_embed(ctx, 'purge')

    @ban.error
    async def ban_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await invalid_perms_embed(ctx, 'ban')

    @kick.error
    async def kick_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await invalid_perms_embed(ctx, 'kick')

    @strike.error
    async def strike_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await invalid_perms_embed(ctx, 'strike')

    @mute.error
    async def mute_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await invalid_perms_embed(ctx, 'mute')

    @unmute.error
    async def unmute_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await invalid_perms_embed(ctx, 'unmute')


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
