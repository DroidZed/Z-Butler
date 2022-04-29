from discord import Guild, Status, Role
from discord.ext.commands import Context


def extract_guild_data(ctx: Context, guild: Guild) -> tuple[list[Role], int, int]:
    roles: list[Role] = list(
        filter(
            lambda role: role != ctx.guild.default_role and not role.managed,
            guild.roles,
        )
    )

    for r in roles:
        if r.id in {
            896349097391444029,
            898875325923094528,
            898874934615482378,
            898874121222516736,
            969706983777263677,
            969639120513163345,
        }:
            del r

    online_users_count: int = len(
        list(
            filter(
                lambda member: member.status != Status.offline and not member.bot,
                guild.members,
            )
        )
    )

    machines_count: int = len(list(filter(lambda member: member.bot, guild.members)))

    return roles, online_users_count, machines_count
