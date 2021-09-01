from tinydb import TinyDB, Query
from discord import Member, Role
from tinydb.table import Document
from tinydb.operations import increment
from discord.ext.commands import Cog, Context, Bot, command
from functions.delete_welcome_image import delete_welcome_image

from config.embed import (
    no_perms_config,
    ban_config,
    strike_config,
    create_embed
)

from config.main import crown_role_id

users = TinyDB('database/db.json').table("users")
UsersQuery = Query()


class ModerationCog(Cog, name="Moderation Commands", description="Mod commands for the admin only."):

    def __init__(self, bot: Bot):
        self.bot = bot

    # ban kick warn

    @command(
        name="ban",
        usage="<username> reason",
        description="Ban a user for a specific reason.")
    async def ban(self, ctx: Context, member: Member = None, reason: str = None):
        """Ban a user for a specific reason."""
        sender_max_role: Role = ctx.message.author.top_role

        if sender_max_role.id != crown_role_id:

            await ctx.send(
                embed=create_embed(
                    config=no_perms_config,
                    no_perms_type='ban'
                )
            )

        elif member is None or member == ctx.message.author:
            await ctx.channel.send("No user provided 🙄 / You cannot ban yourself ⚓")

        else:
            if users.contains((UsersQuery.id == member.id)):
                users.remove(UsersQuery.id == member.id)

            await self._ban_user(ctx, member, reason)

    @command(
        name="kick",
        usage="<username> reason",
        description="Kick a user with a given reason.")
    async def kick(self, ctx: Context, member: Member = None, reason: str = None):
        """Kick a user with a given reason."""
        sender_max_role: Role = ctx.message.author.top_role

        if sender_max_role.id != crown_role_id:

            await ctx.send(
                embed=create_embed(
                    config=no_perms_config,
                    no_perms_type='kick'
                )
            )

        elif member is None or member == ctx.message.author:
            await ctx.channel.send("You cannot kick yourself ⚓ you stupid...")

        elif reason is None:
            await ctx.guild.kick(member, reason='Nothing')
            await ctx.send("Kicked without a reason, not that I care ¯\\_(ツ)_/¯")

        else:
            await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"User > <@{member.id}> has been kicked for: {reason if reason else 'Nothing'} <a:kick:880995293179555852> ")

    @command(
        name="strike",
        usage="<username> reason",
        description="Give a strike to a naughty user.")
    async def strike(self, ctx: Context, member: Member = None, reason: str = None):
        """Give a strike to a naughty user."""
        sender_max_role: Role = ctx.message.author.top_role

        if sender_max_role.id != crown_role_id:

            await ctx.send(
                embed=create_embed(
                    config=no_perms_config,
                    no_perms_type='strike'
                )
            )

        elif member is None or member == ctx.message.author:
            await ctx.channel.send("Why would you strike yourself 🙄 ?")

        else:
            await self._warn_ban_user(ctx, member, reason)

    async def _warn_ban_user(self, ctx: Context, member: Member, reason: str = None):
        found = self.check_member_in_db(member)

        if not found:
            users.insert({'id': member.id, 'strikeCount': 1})
            await member.send(
                embed=create_embed(
                    config=strike_config(2),
                    action='**STRIKE**',
                    reason=reason or '3 Strikes',
                )
            )

        elif users.contains((UsersQuery.id == member.id) & (UsersQuery.strikeCount == 2)):
            users.remove(UsersQuery.id == member.id)

            await self._ban_user(ctx, member, reason)
        else:
            await self._warn_user_for_reason(ctx, member, reason)

    async def _ban_user(self, ctx: Context, member: Member, reason: str = None):
        await member.send(
            embed=create_embed(
                config=ban_config,
                action='**BAN**',
                reason=reason if reason else '3 Strikes'
            )
        )
        delete_welcome_image(member.name)
        await ctx.send(f"User <@{member.id}> has been banned for {reason if reason else '3 Strikes'} 🔨")
        await ctx.guild.ban(member, reason=reason if reason else '3 Strikes')

    async def _warn_user_for_reason(self, ctx: Context, member: Member, reason: str = None):
        res = users.update(
            increment('strikeCount'),
            UsersQuery.id == member.id)[0]

        target: Document = None

        target = users.get(doc_id=res)

        await member.send(
            embed=create_embed(
                config=strike_config(target['strikeCount'] - 1),
                action='***STRIKE***',
                reason=reason or "Nothing",
            )
        )

        await ctx.send("The naughty user has been warned, hope he gets the message 😑")

    def check_member_in_db(self, member):
        return users.search(UsersQuery.id == member.id)


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
