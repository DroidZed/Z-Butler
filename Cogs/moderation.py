from discord import Member, Role, Embed
from discord.ext import commands
from discord.ext.commands import Cog, Context

from config.embed import no_perms_config


class ModerationCog(Cog):

    def __init__(self, bot):
        self.bot = bot

    # ban kick warn

    @commands.command(
        name="ban",
        usage="<username> reason",
        description="Ban a user")
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

            elif reason is None:
                await ctx.guild.ban(member, reason=reason)
                await ctx.send("Banned without a reason, okay whatever...😑")

            else:
                await ctx.guild.ban(member, reason=reason)
                await ctx.send(f'User > <@{member.id}> has been banned with reason: {reason} 🔨')

    @commands.command(
        name="kick",
        usage="<username> reason",
        description="Kick a user")
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

    @commands.command(
        name="warn",
        usage="<username>",
        description="warns a user")
    async def warn(self, ctx: Context, member: Member = None):

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
                await ctx.channel.send("Why would you warn yourself 🙄 ?")
            else:
                await ctx.send("The naughty user has been warned, hope he got the message 😑")


def setup(bot):
    bot.add_cog(ModerationCog(bot))
