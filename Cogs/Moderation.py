from discord import Role
from discord.ext.commands import Bot, Cog, Context, MemberConverter, command
from discord.ext.commands.core import has_role
from discord.ext.commands.errors import CommandError, MissingRole
from tinydb import Query, TinyDB
from tinydb.operations import increment

from config.embed.ban import ban_config
from config.embed.kick import kick_config
from config.embed.no_perms import no_perms_config
from config.embed.strike import strike_config
from config.main import CROWN_ROLE_ID, PREFIX
from functions.embed_factory import create_embed

users = TinyDB('database/db.json').table("users")
UsersQuery = Query()


async def _ban_user(ctx: Context, member: MemberConverter, reason: str):
    users.remove(UsersQuery.id == member.id)
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
    if not users.search(UsersQuery.id == member.id):
        users.insert({'id': member.id, 'strike_count': 1})
        await _strike_user(ctx, member, reason, 2)

    elif users.contains((UsersQuery.id == member.id) & (UsersQuery.strikeCount == 2)):

        await _ban_user(ctx, member, reason)

    else:
        # noinspection PyTypeChecker
        found_member_id = users.update(
            increment('strike_count'),
            UsersQuery.id == member.id)[0]

        await _strike_user(ctx, member, reason, users.get(doc_id=found_member_id)['strike_count'] - 1)


async def invalid_perms_embed(ctx: Context, action: str) -> None:
    await ctx.send(
        embed=create_embed(
            config=no_perms_config(),
            cfg_type=action
        )
    )


def silenced_role(ctx) -> Role:
    return ctx.guild.get_role(896349097391444029)


class ModerationCog(Cog, name="Moderation", description="🏛 Mod commands for **__Lord Lorkhan__** only."):

    _guild = None

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    # ban kick warn purge mute

    @command(
        name="ban",
        usage=f"{PREFIX}ban `username` `reason`",
        description="Ban a user for a specific reason.")
    @has_role(CROWN_ROLE_ID)
    async def ban(self, ctx: Context, member: MemberConverter = None, *reason: str):
        if member is None or member == ctx.message.author:
            await ctx.channel.send("No user provided 🙄 / You cannot ban yourself ⚓")
            return

        else:
            await _ban_user(ctx, member, ' '.join(reason))

    @command(
        name="kick",
        usage=f"{PREFIX}kick `username` `reason`",
        description="Kick a user with a given reason.")
    @has_role(CROWN_ROLE_ID)
    async def kick(self, ctx: Context, member: MemberConverter = None, *reason: str):

        if member is None or member == ctx.message.author:
            await ctx.channel.send(embed=create_embed(kick_config("You cannot kick yourself ⚓ you stupid...")))
            return

        else:
            rs = " ".join(reason) if reason else 'Nothing'
            msg = f"<@{member.id}> has been kicked for {rs} <a:kick:880995293179555852>"
            if not reason:
                msg = "Kicked without a reason, not that I care ¯\\_(ツ)_/¯"
            # noinspection PyTypeChecker
            users.remove(UsersQuery.id == member.id)
            await ctx.guild.kick(member, reason=rs)
            await ctx.send(embed=create_embed(kick_config(msg), rs, None))

    @command(
        name="strike",
        usage=f"{PREFIX}strike `username` `reason`",
        description="Give a strike to a naughty user.")
    @has_role(CROWN_ROLE_ID)
    async def strike(self, ctx: Context, member: MemberConverter = None, *reason: str):
        if member is None or member == ctx.message.author:
            await ctx.channel.send("Why would you strike yourself 🙄 ?")
            return

        else:
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
        usage=f"{PREFIX}mute `username",
        description="Mutes a member.")
    @has_role(CROWN_ROLE_ID)
    async def mute(self, ctx: Context, member: MemberConverter):

        if member.top_role == silenced_role(ctx):
            await ctx.message.reply("User already muted you dump fuck !", delete_after=1.8)
            return

        await member.add_roles(silenced_role(ctx))
        await ctx.send(f":white_check_mark: Muted {member.mention}. Take the time to seek help.",
                       delete_after=1.2)

    @command(
        name="!mute",
        usage=f"{PREFIX}!mute `username`",
        description="UNmutes a muted member.")
    @has_role(CROWN_ROLE_ID)
    async def unmute(self, ctx: Context, member: MemberConverter):

        if member.top_role != silenced_role(ctx):
            await ctx.message.reply("User already unmuted...what a waste of time 🙄", delete_after=1.8)
            return

        await member.remove_roles(silenced_role(ctx))

        await ctx.send(f":white_check_mark: {member.mention} was unmuted. Hopefully you've reflected on your actions.",
                       delete_after=1.2)

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


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
