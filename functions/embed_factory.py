from discord import Embed


def create_embed(
        config: dict,
        reason: str = None,
        no_perms_type: str = None,
        **fields: str) -> Embed:

    embed = init_embed(config)

    embed.set_author(name=config['author']['name'],
                     icon_url=config['author']['icon_url'])

    if fields:

        for f, v in fields.items():

            embed.add_field(
                name=f,
                value=v or '`Nothing to show...`',
                inline=(reason != None)
            )

    if 'thumbnail_url' in config:

        embed.set_thumbnail(
            url=config["thumbnail_url"]
        )

    if reason:

        embed.add_field(
            name="Reason", value=reason or "No reason given", inline=True)

    if 'image_url' in config:

        embed.set_image(url=config["image_url"])

    if no_perms_type:

        embed.set_footer(
            text=config['footer'][no_perms_type]['text'],
            icon_url=config['footer'][no_perms_type]['url']
        )

    if not no_perms_type and 'footer' in config:
        embed.set_footer(
            text=config['footer']['text'],
            icon_url=config['footer']['url']
        )

    return embed


def init_embed(config: dict) -> Embed:

    if ('url' not in config) & ('description' not in config):

        return Embed(
            title=config['title'],
            color=config['color'])

    elif ('url' in config) & ('description' not in config):

        return Embed(
            title=config['title'],
            url=config['url'],
            color=config['color'])

    elif ('url' not in config) & ('description' in config):

        return Embed(
            title=config['title'],
            description=config['description'],
            color=config['color'])

    else:

        return Embed(
            title=config['title'],
            url=config['url'],
            description=config['description'],
            color=config['color'])
