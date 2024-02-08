from typing import Optional

from discord import Guild, Member, Status
from discord.ext.commands import (
    Bot,
    Cog,
    Context,
    command,
    cooldown,
    BucketType,
    is_owner,
)

from utils import Env

from modules.embedder import generate_embed
from utils.helpers import extract_guild_data

from discord.ext.tasks import loop

from modules.embedder.zembed_models import ZembedField


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
                    ZembedField(
                        "\u200b      ", f"***🤖 Machines*** {machines} "
                    ),
                    ZembedField(
                        "\u200b       ", f"***🎖 Ranks*** {roles_count} "
                    ),
                    ZembedField(
                        "\u200b", f"***😜 Emojis*** {len(self.bot.emojis)} "
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

    @command(
        name="ass",
        description="Activate server stats.",
        usage=f"{Env.PREFIX}ass",
    )
    @cooldown(1, 2, BucketType.user)
    async def activate_stat_updater(self, ctx: Context):
        self.update_voice_channel_counts.start()

    @loop(minutes=1)
    @is_owner()
    async def update_voice_channel_counts(self):
        THE_CIRCLE_ROLE_ID = 1203610897839562783

        DUTY_TEAM_IDS = {
            "onduty": 1204180776212631582,
            "offduty": 1204180800111648769,
        }

        MOD_TEAM_IDS = {
            "repteam": 1203600733195477013,
            "verifyteam": 1203600802279718912,
        }

        CHANNEL_DUTY_IDS = {
            "verifychannel": 1204760925257728040,
            "repchannel": 1204760745213038673,
        }

        team_counts = {"repteam": 0, "verifyteam": 0}
        guild = self.bot.guilds[0]

        admins_online_list = list(
            filter(
                lambda member: member.status != Status.offline
                and member.status != Status.invisible
                and len(
                    set(MOD_TEAM_IDS.keys()).intersection(set(member.roles))
                )
                and not member.bot,
                guild.members,
            )
        )

        on_duty_count = len(
            [
                member
                for member in admins_online_list
                if DUTY_TEAM_IDS["onduty"]
                in list(map(lambda r: r.id, member.roles))
            ]
        )

        off_duty_count = len(
            [
                member
                for member in admins_online_list
                if DUTY_TEAM_IDS["onduty"]
                in list(map(lambda r: r.id, member.roles))
            ]
        )

        on_duty_channel = list(
            filter(
                lambda channel: channel.id == CHANNEL_DUTY_IDS["verifychannel"],
                guild.voice_channels,
            )
        )[0]

        off_duty_channel = list(
            filter(
                lambda channel: channel.id == CHANNEL_DUTY_IDS["repchannel"],
                guild.voice_channels,
            )
        )[0]

        if on_duty_channel is not None:
            await on_duty_channel.edit(name=f"ON DUTY {on_duty_count} HERE")

        if off_duty_channel is not None:
            await off_duty_channel.edit(name=f"OFF DUTY {off_duty_count} HERE")


def setup(bot: Bot):
    bot.add_cog(StatsCog(bot))
