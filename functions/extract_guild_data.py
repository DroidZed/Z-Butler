from discord import Guild, Status, Role
from discord.ext.commands import Context


def extract_guild_data(ctx: Context, guild: Guild) -> tuple[list[Role], int, int]:
    """Extracts some useful data from the server.

    Params:
    ------------
    ctx: :class:`Context`
        The context to which the user sent the command to.

    guild :class:`Guild`
        The guild we belong to.

    Returns:
    ------------
    Human roles present in the guild: :class:`list[Roles]`

    Online users count: :class:`int`

    Bots count: :class:`int`    
    """

    roles: list[Role] = list(
        filter(
            lambda role: role != ctx.guild.default_role and not role.managed, guild.roles)
    )

    online_users_count: int = len(
        list(
            filter(
                lambda member: member.status != Status.offline and not member.bot, guild.members)
        )
    )

    machines_count: int = len(
        list(
            filter(
                lambda member: member.bot, guild.members)
        )
    )

    return roles, online_users_count, machines_count
