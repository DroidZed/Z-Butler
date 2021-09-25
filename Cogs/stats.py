from discord import Guild, Embed, Member
from discord.ext.commands import (Bot, Cog, Context, MemberConverter, command,
                                  cooldown)
from discord.ext.commands.cooldowns import BucketType

from config.embed.server import server_stats_config
from config.embed.user_stats import user_stats
from config.main import GUILD_ID, PREFIX
from functions.embed_factory import create_embed
from functions.extract_guild_data import extract_guild_data


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
        async with ctx.typing():
            guild: Guild = self.bot.get_guild(GUILD_ID)

            roles, online_users_count, machines = extract_guild_data(
                ctx, guild)

            data = {
                "Lord": "𝕯𝖗𝖔𝖎𝖉𝖅𝖊𝖉",
                "Heads Count": f"{guild.member_count - machines} dragons",
                "Dens": f"💬 {len(guild.text_channels)} & 🎶 {len(guild.voice_channels)}",
                "Established at": f"{guild.created_at.strftime('%b %d %Y %H:%M:%S')}",
                "🟢 Alive": f"{online_users_count} (**{round((online_users_count / guild.member_count * 100))}%**)",
                "🤖 Machines": f"{machines}",
                "Ranks": " ".join(role.mention for role in roles[::-1]),
            }

            embed = create_embed(config=server_stats_config(
                title=guild.name), reason=None, cfg_type='stats', **data)

        await ctx.send(embed=embed)

    @command(name="user_stats",
             description="Grabs the request user's info.",
             usage=f"{PREFIX}user `username`",
             aliases=['user?', 'u?']
             )
    @cooldown(1, 2, BucketType.user)
    async def user_stats(self, ctx: Context, member: MemberConverter = None) -> None:
        member = member or ctx.message.author

        fields = {
            "Created at": f"{member.created_at.strftime('%b %d %Y')}",
            "Joined at": f"{member.joined_at.strftime('%b %d %Y')}",
            "Nickname": f"{member.nick}",
            "Top Rank": f"{member.top_role.mention}",
            "Ranks": " ".join(r.mention for r in member.roles if not r.is_default()),

        }

        embed: Embed = create_embed(
            user_stats(
                member.name,
                member.mention,
                str(str(member.avatar_url))),
            None,
            'stats',
            **fields)

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
