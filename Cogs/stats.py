from config.embed.user_stats import user_stats
from discord.ext.commands.cooldowns import BucketType
from config.embed.server import server_stats_config
from functions.embed_factory import create_embed
from discord import Guild, Role, Member, Status
from discord.ext.commands import (
    cooldown,
    Bot,
    Cog,
    command,
    Context
)
from config.main import GUILD_ID, PREFIX
from pprint import pprint


class StatsCog(Cog, name="Server Stats", description="Stats for nerds."):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="server",
             description="Grabs the server's info.",
             usage=f"{PREFIX}server",
             aliases=['info', 's?']
             )
    @cooldown(1, 2, BucketType.user)
    async def server_info(self, ctx: Context):

        guild: Guild = self.bot.get_guild(GUILD_ID)

        roles: list[Role] = [role for role in guild.roles if role !=
                             ctx.guild.default_role and not role.managed]

        alive_humans = sum(
            member for member in guild.members if member.status != Status.offline and not member.bot)

        machines = sum(member.bot for member in guild.members)

        humans_count = guild.member_count - machines

        data = {
            "Lord": "𝕯𝖗𝖔𝖎𝖉𝖅𝖊𝖉",
            "Heads Count": f"{humans_count} dragons",
            "Dens": f"💬 {len(guild.text_channels)} & 🎶 {len(guild.voice_channels)}",
            "Established at": f"{guild.created_at.strftime('%b %d %Y %H:%M:%S')}",
            "🟢 Alive": f"{alive_humans} (**{round((alive_humans / guild.member_count * 100))}%**)",
            "🤖 Machines": f"{machines}",
            "Ranks": " ".join(role.mention for role in roles[::-1]),
        }

        embed = create_embed(config=server_stats_config(
            title=guild.name), reason=None, cfg_type='stats', **data)

        await ctx.send(embed=embed)

    @command(name="user_status",
             description="Grabs the request user's info.",
             usage=f"{PREFIX}user <username>",
             aliases=['user?', 'u?']
             )
    @cooldown(1, 2, BucketType.user)
    async def user_stats(self, ctx: Context, member: Member = None) -> None:

        member = member or ctx.author

        fields = {
            "Created at": f"{member.created_at.strftime('%b %d %Y')}",
            "Joined at": f"{member.joined_at.strftime('%b %d %Y')}",
            "Nickname": f"{member.nick}",
            "Top Rank": f"{member.top_role.mention}",
            "Ranks": " ".join(r.mention for r in member.roles if not r.is_default()),

        }

        await ctx.send(embed=create_embed(
            user_stats(
                member.name,
                member.mention,
                member.avatar_url),
            None,
            'stats',
            **fields)
        )


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
