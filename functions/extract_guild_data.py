from discord import Guild, Status


def extract_guild_data(guild: Guild) -> tuple[int, int, int]:

    roles_count: int = len(guild.roles)

    online_users_count: int = len(
        list(
            filter(
                lambda member: member.status != Status.offline and not member.bot,
                guild.members,
            )
        )
    )

    machines_count: int = len(list(filter(lambda member: member.bot, guild.members)))

    return roles_count, online_users_count, machines_count
