from tinydb import TinyDB, Query
from discord import Member, Role, Embed
from tinydb.operations import increment
from discord.ext.commands import Cog, Context, Bot, command
from tinydb.table import Document

from config.embed import *

db = TinyDB('database/db.json')
Users = Query()


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

        if sender_max_role.id != 778285282872393769:
            # await ctx.send("You're not powerful enough to use this command, how pifitul 😒")
            embed = Embed(
                title=no_perms_config['title'],
                url=no_perms_config['url'],
                description=no_perms_config['description'],
                color=no_perms_config['color']
            )

            embed.set_author(
                name=no_perms_config['author']['name'],
                icon_url=no_perms_config['author']['icon_url']
            )

            embed.set_image(url=no_perms_config["image_url"])

            embed.set_thumbnail(url=no_perms_config["thumbnail_url"])

            embed.set_footer(
                text=no_perms_config['footer']['ban']['text'],
                icon_url=no_perms_config['footer']['ban']['url']
            )

            await ctx.send(embed=embed)

        else:
            if member is None or member == ctx.message.author:
                await ctx.channel.send("No user provided 🙄 / You cannot ban yourself ⚓")
            else:
                if db.contains((Users.id == member.id)):
                    db.remove(Users.id == member.id)

                    await member.send(
                        embed=self._createEmbed(
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

        if sender_max_role.id != 778285282872393769:
            # await ctx.send("You're not powerful enough to use this command, how pifitul 😒")
            embed = Embed(
                title=no_perms_config['title'],
                url=no_perms_config['url'],
                description=no_perms_config['description'],
                color=no_perms_config['color']
            )

            embed.set_author(
                name=no_perms_config['author']['name'],
                icon_url=no_perms_config['author']['icon_url']
            )

            embed.set_image(url=no_perms_config["image_url"])

            embed.set_thumbnail(url=no_perms_config["thumbnail_url"])

            embed.set_footer(
                text=no_perms_config['footer']['kick']['text'],
                icon_url=no_perms_config['footer']['kick']['url']
            )

            await ctx.send(embed=embed)

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
        description="Give a strike to a naughty user")
    async def strike(self, ctx: Context, member: Member = None, reason: str = None):

        sender_max_role: Role = ctx.message.author.top_role

        if sender_max_role.id != 778285282872393769:
            # await ctx.send("You're not powerful enough to use this command, how pifitul 😒")
            embed = Embed(
                title=no_perms_config['title'],
                url=no_perms_config['url'],
                description=no_perms_config['description'],
                color=no_perms_config['color']
            )

            embed.set_author(
                name=no_perms_config['author']['name'],
                icon_url=no_perms_config['author']['icon_url']
            )

            embed.set_image(url=no_perms_config["image_url"])

            embed.set_thumbnail(url=no_perms_config["thumbnail_url"])

            embed.set_footer(
                text=no_perms_config['footer']['warn']['text'],
                icon_url=no_perms_config['footer']['warn']['url']
            )

            await ctx.send(embed=embed)

        else:

            if member is None or member == ctx.message.author:
                await ctx.channel.send("Why would you strike yourself 🙄 ?")

            else:
                found = db.search(Users.id == member.id)

                if not found:
                    db.insert({'id': member.id, 'strikeCount': 1})
                    await member.send(
                        embed=self._createEmbed(
                            config=strike_config(2),
                            action='**STRIKE**',
                            reason=reason if reason else '3 Strikes'
                        )
                    )

                else:
                    if db.contains((Users.id == member.id) & (Users.strikeCount == 2)):
                        db.remove(Users.id == member.id)

                        await member.send(
                            embed=self._createEmbed(
                                config=ban_config,
                                action='**BAN**',
                                reason=reason if reason else '3 Strikes'
                            )
                        )
                        await ctx.send(f"User <@{member.id}> has been banned for {reason if reason else '3 Strikes'} 🔨")
                        await ctx.guild.ban(member, reason=reason if reason else '3 Strikes')
                    else:
                        res = db.update(
                            increment('strikeCount'),
                            Users.id == member.id
                        )[0]

                        target: Document = None

                        target = db.get(doc_id=res)

                        await member.send(
                            embed=self._createEmbed(
                                config=strike_config(target['strikeCount']-1),
                                action='***STRIKE***',
                                reason=reason if reason else "Nothing"
                            )
                        )
                        await ctx.send("The naughty user has been warned, hope he gets the message 😑")

    def _createEmbed(self, reason, config, action):
        embed = Embed(
            title=config['title'],
            url=config['url'],
            description=config['description'],
            color=config['color']
        )

        embed.set_author(
            name=config['author']['name'],
            icon_url=config['author']['icon_url']
        )

        embed.add_field(
            name="Action",
            value=action,
            inline=True
        )

        embed.add_field(
            name="Reason",
            value=reason if reason else "No reason given",
            inline=True
        )

        embed.set_footer(
            text=config['footer']['text'],
            icon_url=config['footer']['url']
        )

        return embed


def setup(bot: Bot):
    bot.add_cog(ModerationCog(bot))
