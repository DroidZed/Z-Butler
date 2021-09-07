from config.embed.kick import kick_config
from config.embed.ban import ban_config
from config.embed.no_perms import no_perms_config
from config.embed.strike import strike_config
from config.main import CROWN_ROLE_ID, PREFIX
from discord import Member
from discord.ext.commands import Bot, Cog, Context, command
from discord.ext.commands.core import has_role
from discord.ext.commands.errors import CommandError, MissingRole
from functions.embed_factory import create_embed
from tinydb import Query, TinyDB
from tinydb.operations import increment
from tinydb.table import Document

users = TinyDB('database/db.json').table("users")
UsersQuery = Query()


class ModerationCog(Cog, name="Moderation Commands", description="Mod commands for the admin only."):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    # ban kick warn purge

    @command(
        name="ban",
        usage=f"{PREFIX}ban `username` `reason`",
        description="Ban a user for a specific reason.")
    @has_role(CROWN_ROLE_ID)
    async def ban(self, ctx: Context, member: Member = None, *reason: str):
        if member is None or member == ctx.message.author:
            await ctx.channel.send("No user provided 🙄 / You cannot ban yourself ⚓")
            return

        else:
            await self._ban_user(ctx, member,  ' '.join(reason))

    @command(
        name="kick",
        usage=f"{PREFIX}kick `username` `reason`",
        description="Kick a user with a given reason.")
    @has_role(CROWN_ROLE_ID)
    async def kick(self, ctx: Context, member: Member = None, *reason: str):

        if member is None or member == ctx.message.author:
            await ctx.channel.send(embed=create_embed(kick_config("You cannot kick yourself ⚓ you stupid...")))
            return

        else:
            rs = " ".join(reason) if reason else 'Nothing'
            msg = f"<@{member.id}> has been kicked for {rs} <a:kick:880995293179555852>"
            if not reason:
                msg = "Kicked without a reason, not that I care ¯\\_(ツ)_/¯"
            users.remove(UsersQuery.id == member.id)
            await ctx.guild.kick(member, reason=rs)
            await ctx.send(embed=create_embed(kick_config(msg), rs, None))

    @command(
        name="strike",
        usage=f"{PREFIX}strike `username` `reason`",
        description="Give a strike to a naughty user.")
    @has_role(CROWN_ROLE_ID)
    async def strike(self, ctx: Context, member: Member = None, *reason: str):
        if member is None or member == ctx.message.author:
            await ctx.channel.send("Why would you strike yourself 🙄 ?")
            return

        else:
            await self._strike_ban_user(ctx, member,  ' '.join(reason))

    @command(
        name="purge",
        usage=f"{PREFIX}purge `amount`",
        description="Clears a certain amount of messages, can't delete those older than 14 days though.")
    @has_role(CROWN_ROLE_ID)
    async def purge(self, ctx: Context, amount: int):
        await ctx.channel.purge(limit=amount)

    async def _strike_ban_user(self, ctx: Context, member: Member, reason: str):

        if not users.search(UsersQuery.id == member.id)[0]:
            users.insert({'id': member.id, 'strike_count': 1})
            await self._strike_user(ctx, member, reason, 2)

        elif users.contains((UsersQuery.id == member.id) & (UsersQuery.strikeCount == 2)):

            await self._ban_user(ctx, member, reason)

        else:
            found_member_id = users.update(
                increment('strike_count'),
                UsersQuery.id == member.id)[0]

            await self._strike_user(ctx, member, reason, users.get(doc_id=found_member_id)['strikeCount'] - 1)

    async def _ban_user(self, ctx: Context, member: Member, reason: str):
        users.remove(UsersQuery.id == member.id)
        await member.send(
            embed=create_embed(
                config=ban_config,
                reason=reason or "3 Strikes",
                no_perms_type=None,
                Action='**BAN**'
            )
        )
        await ctx.send(f"User <@{member.id}> has been banned for {reason or '3 Strikes'} 🔨")
        await ctx.guild.ban(member, reason=reason or '3 Strikes')

    async def _strike_user(self, ctx: Context, member: Member, reason: str, strikes: int):

        await member.send(
            embed=create_embed(
                config=strike_config(strikes),
                reason=reason or "Nothing",
                no_perms_type=None,
                Action='***STRIKE***',
            )
        )

        await ctx.send("The naughty user has been warned, hope he gets the message 😑")

    # error handlers
    @purge.error
    async def purge_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await self.invalid_perms_embed(ctx, 'purge')

    @ban.error
    async def ban_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await self.invalid_perms_embed(ctx, 'ban')

    @kick.error
    async def kick_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await self.invalid_perms_embed(ctx, 'kick')

    @strike.error
    async def strike_handler(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRole):
            await self.invalid_perms_embed(ctx, 'strike')

    # util functions
    async def invalid_perms_embed(self, ctx: Context, action: str) -> None:
        await ctx.send(
            embed=create_embed(
                config=no_perms_config,
                no_perms_type=action
            )
        )


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
