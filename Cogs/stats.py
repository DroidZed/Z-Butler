from discord import Guild
from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    Member,
    command,
    cooldown,
    BucketType,
)

from classes.embed_factory import EmbedFactory
from config.colors import BOT_COLOR
from config.links import server_image
from config.main import GUILD_ID, PREFIX, OWNER_ID
from functions.helpers import extract_guild_data


class StatsCog(Cog, name="Stats", description="Stats for nerds."):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="server",
        description="Grabs the server's info.",
        usage=f"{PREFIX}server",
        aliases=["s?"],
    )
    @cooldown(1, 2, BucketType.user)
    async def server_info(self, ctx: Context):
        async with ctx.typing():
            guild: Guild = self.bot.get_guild(GUILD_ID)

            roles_count, online_users_count, machines, desc = extract_guild_data(guild)

            data = {
                "\u200b ": f"***🐲 Lord*** [𝕯𝖗𝖔𝖎𝖉𝖅𝖊𝖉](https://discord.com/users/{OWNER_ID})",
                "\u200b  ": f"***🗿 Headcount*** {guild.member_count - machines}",
                "\u200b   ": f"***🏘 Dens*** 💬 {len(guild.text_channels)} & 🎶 {len(guild.voice_channels)}",
                "\u200b    ": f"***📅 Established at*** {guild.created_at.strftime('%b %d %Y')}",
                "\u200b     ": f"🟢 ***Alive members*** {online_users_count}"
                               f" (**{round((online_users_count / guild.member_count * 100))}%**)",
                "\u200b      ": f"***🤖 Machines*** {machines} ",
                "\u200b       ": f"***🎖 Ranks*** {roles_count} ",
                "\u200b": f"***😜 Emojis*** {len(self.bot.emojis)} ",
            }

            embed = EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    color=BOT_COLOR,
                    description=desc,
                    thumbnail={
                        "url": server_image
                    },
                    author={"name": guild.name},
                    footer={
                        "text": "From the best bot ever, of the best server ever 💙",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                ),
                reason=None,
                cfg_type="stats",
                **data,
            )

        await ctx.send(embed=embed)

    @command(
        name="user",
        description="Grabs the request user's info.",
        usage=f"{PREFIX}user `username`",
        aliases=["u?"],
    )
    @cooldown(1, 2, BucketType.user)
    async def user_stats(self, ctx: Context, member: Member = None) -> None:
        member = member or ctx.message.author

        await ctx.send(
            embed=EmbedFactory.create_embed(
                config=EmbedFactory.create_config(
                    title=f"**{member.name}**'s Stats",
                    description=f"{member.mention}'s information.",
                    color=BOT_COLOR,
                    author={
                        "name": "The Z Butler",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586"
                                    "/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                    thumbnail={"url": member.avatar_url},
                    footer={
                        "text": "Delivered by your trusty bot, Z Butler 💙",
                        "icon_url": "https://cdn.discordapp.com/avatars/759844892443672586"
                                    "/bb7df4730c048faacd8db6dd99291cdb.jpg",
                    },
                ),
                cfg_type="stats",
                **{
                    "Created at": f"{member.created_at.strftime('%b %d %Y')}",
                    "Joined at": f"{member.joined_at.strftime('%b %d %Y')}",
                    "Nickname": f"{member.nick}",
                    "Top Rank": f"{member.top_role.mention}",
                    "Ranks": " ".join(r.mention for r in member.roles if not r.is_default()),
                },
            )
        )


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
