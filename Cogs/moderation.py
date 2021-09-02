from discord.ext.commands.core import has_role
from discord.ext.commands.errors import CommandError
from tinydb import TinyDB, Query
from discord import Member
from tinydb.table import Document
from tinydb.operations import increment
from discord.ext.commands import Cog, Context, Bot, command

from config.embed import (
    ban_config,
    strike_config
)

from config.embed import no_perms_config

from functions.embed_factory import create_embed

from config.main import crown_role_id

users = TinyDB('database/db.json').table("users")
UsersQuery = Query()


class ModerationCog(Cog, name="Moderation Commands", description="Mod commands for the admin only."):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    # ban kick warn

    @command(
        name="ban",
        usage="<username> reason",
        description="Ban a user for a specific reason.")
    @has_role(crown_role_id)
    async def ban(self, ctx: Context, member: Member = None, *reason: str):
        """Ban a user for a specific reason."""
        if member is None or member == ctx.message.author:
            await ctx.channel.send("No user provided 🙄 / You cannot ban yourself ⚓")
            return

        else:
            if users.contains((UsersQuery.id == member.id)):
                users.remove(UsersQuery.id == member.id)

            await self._ban_user(ctx, member, reason)

    @command(
        name="kick",
        usage="<username> reason",
        description="Kick a user with a given reason.")
    @has_role(crown_role_id)
    async def kick(self, ctx: Context, member: Member = None, *reason: str):
        """Kick a user with a given reason."""
        if member is None or member == ctx.message.author:
            await ctx.channel.send("You cannot kick yourself ⚓ you stupid...")
            return

        elif reason is None:
            await ctx.guild.kick(member, reason='Nothing')
            await ctx.send("Kicked without a reason, not that I care ¯\\_(ツ)_/¯")

        else:
            rs = " ".join(reason)
            await ctx.guild.kick(member, reason=rs)
            await ctx.send(f"User > <@{member.id}> has been kicked for {rs if reason else 'Nothing'} <a:kick:880995293179555852> ")

    @command(
        name="strike",
        usage="<username> reason",
        description="Give a strike to a naughty user.")
    @has_role(crown_role_id)
    async def strike(self, ctx: Context, member: Member = None, *reason: str):
        """Give a strike to a naughty user."""
        if member is None or member == ctx.message.author:
            await ctx.channel.send("Why would you strike yourself 🙄 ?")
            return

        else:
            await self._strike_ban_user(ctx, member, reason)

    @command(
        name="purge",
        usage="amount",
        description="Clears a certain amount of messages, can't delete those older than 14 days tho.")
    @has_role(crown_role_id)
    async def purge(self, ctx: Context, amount: int):
        """ Clears a certain amount of messages, can't delete those older than 14 days tho. """
        await ctx.channel.purge(limit=amount)

    async def _strike_ban_user(self, ctx: Context, member: Member, *reason: str):
        found = self._check_member_in_db(member)

        if not found:
            users.insert({'id': member.id, 'strikeCount': 1})

            await member.send(
                embed=create_embed(
                    config=strike_config(2),
                    action='**STRIKE**',
                    reason=" ".join(reason) if reason else 'Nothing',
                )
            )
            await ctx.send("The naughty user has been warned, hope he gets the message 😑")

        elif users.contains((UsersQuery.id == member.id) & (UsersQuery.strikeCount == 2)):
            users.remove(UsersQuery.id == member.id)

            await self._ban_user(ctx, member, reason)
        else:
            await self._strike_user(ctx, member, reason)

    async def _ban_user(self, ctx: Context, member: Member, *reason: str):
        rs = " ".join(reason)
        await member.send(
            embed=create_embed(
                config=ban_config,
                action='**BAN**',
                reason=rs if reason else '3 Strikes'
            )
        )
        await ctx.send(f"User <@{member.id}> has been banned for {rs if reason else '3 Strikes'} 🔨")
        await ctx.guild.ban(member, reason=rs if reason else '3 Strikes')

    async def _strike_user(self, ctx: Context, member: Member, *reason: str):

        found_member_id = users.update(
            increment('strikeCount'),
            UsersQuery.id == member.id)[0]

        target: Document = users.get(doc_id=found_member_id)

        rs = " ".join(reason)

        await member.send(
            embed=create_embed(
                config=strike_config(target['strikeCount'] - 1),
                action='***STRIKE***',
                reason=rs or "Nothing",
            )
        )

        await ctx.send("The naughty user has been warned, hope he gets the message 😑")

    def _check_member_in_db(self, member):
        return users.search(UsersQuery.id == member.id)

    @purge.error
    async def purge_handler(self, ctx: Context, error: CommandError) -> None:
        await self.invalid_perms_embed(ctx, 'purge')

    @ban.error
    async def ban_handler(self, ctx: Context, error: CommandError) -> None:
        await self.invalid_perms_embed(ctx, 'ban')

    @kick.error
    async def kick_handler(self, ctx: Context, error: CommandError) -> None:
        await self.invalid_perms_embed(ctx, 'kick')

    @strike.error
    async def strike_handler(self, ctx: Context, error: CommandError) -> None:
        await self.invalid_perms_embed(ctx, 'strike')

    async def invalid_perms_embed(self, ctx: Context, action: str) -> None:
        await ctx.send(
            embed=create_embed(
                config=no_perms_config,
                no_perms_type=action
            )
        )


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
