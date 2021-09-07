from config.embed.server import server_stats_config
from functions.embed_factory import create_embed
from discord import (Embed, Member, Guild, Role)
from discord.ext.commands import (
    cooldown,
    Bot,
    Cog,
    command,
    Context
)
from config.main import GUILD_ID, PREFIX


class StatsCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="server",
             description="Grabs the server's info.",
             usage=f"{PREFIX}server",
             aliases=['info', 's?']
             )
    async def server_info(self, ctx: Context):

        guild: Guild = self.bot.get_guild(GUILD_ID)

        await ctx.send(f'{ctx.message.author.top_role.color=}')

        data = {
            "Server members": guild.member_count,
            "Lord": "𝕯𝖗𝖔𝖎𝖉𝖅𝖊𝖉",
            "Channels": f"Txt: {len(guild.text_channels)} / Vc: {len(guild.voice_channels)}"
        }

        embed = create_embed(server_stats_config(
            title=guild.name), None, None, **data)

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
