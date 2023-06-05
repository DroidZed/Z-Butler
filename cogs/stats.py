from typing import Optional

from discord import Guild, Member
from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
    cooldown,
    BucketType,
)

from utils import Env

from modules.embedder import generate_embed
from utils.helpers import extract_guild_data

from modules.embedder.zembed_models import ZembedField


class StatsCog(
    Cog, name="Stats", description="Stats for nerds."
):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        name="server",
        description="Grabs the server's info.",
        usage=f"{Env.PREFIX}server",
        aliases=["s?"],
    )
    @cooldown(1, 2, BucketType.user)
    async def server_info(self, ctx: Context):
        async with ctx.typing():
            guild: Guild | None = self.bot.get_guild(
                Env.GUILD_ID
            )

            if guild:
                (
                    roles_count,
                    online_users_count,
                    machines,
                ) = extract_guild_data(
                    guild.roles,
                    guild.members,
                )

                data = [
                    ZembedField(
                        "\u200b ",
                        f"***🐲 Lord*** [𝕯𝖗𝖔𝖎𝖉𝖅𝖊𝖉](https://discord.com/users/{Env.OWNER_ID})",
                    ),
                    ZembedField(
                        "\u200b  ",
                        f"***🗿 Headcount*** {guild.member_count - machines}",
                    ),
                    ZembedField(
                        "\u200b   ",
                        f"***🏘 Dens*** 💬 {len(guild.text_channels)} & 🎶 {len(guild.voice_channels)}",
                    ),
                    ZembedField(
                        "\u200b    ",
                        f"***📅 Established at*** {guild.created_at.strftime('%b %d %Y')}",
                    ),
                    ZembedField(
                        "\u200b     ",
                        f"🟢 ***Alive members*** {online_users_count} (**{round((online_users_count / guild.member_count * 100))}%**)",
                    ),
                    ZembedField(
                        "\u200b      ",
                        f"***🤖 Machines*** {machines} ",
                    ),
                    ZembedField(
                        "\u200b       ",
                        f"***🎖 Ranks*** {roles_count} ",
                    ),
                    ZembedField(
                        "\u200b",
                        f"***😜 Emojis*** {len(self.bot.emojis)} ",
                    ),
                ]

                await ctx.send(
                    embed=generate_embed(
                        None,
                        guild.description,
                        None,
                        guild.name,
                        None,
                        None,
                        None,
                        None,
                        "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
                        "From the best bot ever, of the best server ever 💙",
                        False,
                        *data,
                    )
                )

    @command(
        name="user",
        description="Grabs the request user's info.",
        usage=f"{Env.PREFIX}user `username`",
        aliases=["u?"],
    )
    @cooldown(1, 2, BucketType.user)
    async def user_stats(
        self, ctx: Context, member: Optional[Member] = None
    ) -> None:
        found = member or ctx.message.author

        data = [
            ZembedField(
                "Created at",
                f"{found.created_at.strftime('%b %d %Y')}",
            ),
            ZembedField(
                "Nickname",
                f"{found.nick}",  # type: ignore
            ),
            ZembedField(
                "Top Rank",
                f"{found.top_role.mention}",  # type: ignore
            ),
            ZembedField(
                "Ranks",
                " ".join(
                    r.mention
                    for r in found.roles  # type: ignore
                    if not r.is_default()
                ),
            ),
        ]

        embed = generate_embed(
            f"**{found.name}**'s Stats",
            f"{found.mention}'s information.",
            Env.BOT_COLOR,
            None,
            None,
            None,
            found.avatar.url if found.avatar else "",
            None,
            "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
            "Delivered by your trusty bot, Z Butler 💙",
            False,
            *data,
        )

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
