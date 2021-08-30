from tinydb import TinyDB, Query
from discord import Member, Role
from tinydb.table import Document
from tinydb.operations import increment
from discord.ext.commands import Cog, Context, Bot, command

from config.embed import (
    no_perms_config,
    ban_config,
    strike_config,
    createEmbed
)

from config.main import crown_role_id

users = TinyDB('database/db.json').table("users")
UsersQuery = Query()


class ModerationCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    # ban kick warn

    @command(
        name="ban",
        usage="<username> reason",
        description="Ban a user for a specific reason.")
    async def ban(self, ctx: Context, member: Member = None, reason: str = None):

        sender_max_role: Role = ctx.message.author.top_role

        if sender_max_role.id != crown_role_id:

            await ctx.send(
                embed=createEmbed(
                    config=no_perms_config,
                    no_perms_type='ban'
                )
            )

        else:
            if member is None or member == ctx.message.author:
                await ctx.channel.send("No user provided 🙄 / You cannot ban yourself ⚓")
            else:
                if users.contains((UsersQuery.id == member.id)):
                    users.remove(UsersQuery.id == member.id)

                await member.send(
                    embed=createEmbed(
                        config=ban_config,
                        action='**BAN**',
                        reason=reason if reason else 'Nothing'
                    )
                )

                await ctx.guild.ban(member, reason=reason if reason else 'Nothing')
                await ctx.send(f"User <@{member.id}> has been banned for {reason if reason else 'Nothing'} 🔨")

    @command(
        name="kick",
        usage="<username> reason",
        description="Kick a user with a given reason.")
    async def kick(self, ctx: Context, member: Member = None, reason: str = None):

        sender_max_role: Role = ctx.message.author.top_role

        if sender_max_role.id != crown_role_id:

            await ctx.send(
                embed=createEmbed(
                    config=no_perms_config,
                    no_perms_type='kick'
                )
            )

        else:

            if member is None or member == ctx.message.author:
                await ctx.channel.send("No user provided 🙄 / You cannot kick yourself ⚓")

            elif reason is None:
                await ctx.guild.kick(member, reason=reason)
                await ctx.send("Kicked without a reason, not that I care ¯\_(ツ)_/¯")

            else:
                await ctx.guild.kick(member, reason=reason)
                await ctx.send(f'User > <@{member.id}> has been kicked with reason: {reason} :kick: ')

    @command(
        name="strike",
        usage="<username> reason",
        description="Give a strike to a naughty user.")
    async def strike(self, ctx: Context, member: Member = None, reason: str = None):

        sender_max_role: Role = ctx.message.author.top_role

        if sender_max_role.id != crown_role_id:

            await ctx.send(
                embed=createEmbed(
                    config=no_perms_config,
                    no_perms_type='strike'
                )
            )

        else:

            if member is None or member == ctx.message.author:
                await ctx.channel.send("Why would you strike yourself 🙄 ?")

            else:
                found = users.search(UsersQuery.id == member.id)

                if not found:
                    users.insert({'id': member.id, 'strikeCount': 1})
                    await member.send(
                        embed=createEmbed(
                            config=strike_config(2),
                            action='**STRIKE**',
                            reason=reason if reason else '3 Strikes'
                        )
                    )

                else:
                    if users.contains((UsersQuery.id == member.id) & (UsersQuery.strikeCount == 2)):
                        users.remove(UsersQuery.id == member.id)

                        await member.send(
                            embed=createEmbed(
                                config=ban_config,
                                action='**BAN**',
                                reason=reason if reason else '3 Strikes'
                            )
                        )
                        await ctx.send(f"User <@{member.id}> has been banned for {reason if reason else '3 Strikes'} 🔨")
                        await ctx.guild.ban(member, reason=reason if reason else '3 Strikes')
                    else:
                        res = users.update(
                            increment('strikeCount'),
                            UsersQuery.id == member.id
                        )[0]

                        target: Document = None

                        target = users.get(doc_id=res)

                        await member.send(
                            embed=createEmbed(
                                config=strike_config(target['strikeCount']-1),
                                action='***STRIKE***',
                                reason=reason if reason else "Nothing"
                            )
                        )
                        await ctx.send("The naughty user has been warned, hope he gets the message 😑")


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
