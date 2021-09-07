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


class StatsCog(Cog, name="Server Stas", description="Stats for nerds."):

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
            member.status != Status.offline and not member.bot for member in guild.members)

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

        embed = create_embed(server_stats_config(
            title=guild.name), None, None, **data)

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
