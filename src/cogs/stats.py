from typing import List, Optional

from discord import Guild, Member, Role, Status
from discord.ext.commands import (
    Bot,
    BucketType,
    Cog,
    Context,
    command,
    cooldown,
)
from modules.embedder import generate_embed
from modules.embedder.zembed_models import ZembedField
from utils import Env


def extract_guild_data(
    roles: List[Role], members: List[Member]
) -> tuple[int, int, int]:
    roles_count: int = len(roles) - 1

    online_users_count: int = len(
        list(
            filter(
                lambda member: member.status != Status.offline
                and member.status != Status.invisible
                and not member.bot,
                members,
            )
        )
    )

    machines_count: int = len(list(filter(lambda member: member.bot, members)))

    return (
        roles_count,
        online_users_count,
        machines_count,
    )


class StatsCog(Cog, name="Stats", description="Stats for nerds."):
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
            guild: Guild | None = self.bot.get_guild(Env.GUILD_ID)

            if guild:
                roles_count, online_users_count, machines = extract_guild_data(
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
                    ZembedField("\u200b      ", f"***🤖 Machines*** {machines} "),
                    ZembedField("\u200b       ", f"***🎖 Ranks*** {roles_count} "),
                    ZembedField("\u200b", f"***😜 Emojis*** {len(self.bot.emojis)} "),
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
    async def user_stats(self, ctx: Context, member: Optional[Member] = None) -> None:
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
                    for r in found.roles
                    if not r.is_default()  # type: ignore
                ),
            ),
        ]

        embed = generate_embed(
            title=f"**{found.name}**'s Stats",
            description=f"{found.mention}'s information.",
            color=Env.BOT_COLOR,
            thumbnail_url=found.avatar.url if found.avatar else "",
            footer_icon="https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg",
            footer_text="Delivered by your trusty bot, Z Butler 💙",
            rem_img=False,
            *data,
        )

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
