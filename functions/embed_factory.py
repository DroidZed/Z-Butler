from discord import Embed


def create_embed(
        config: dict,
        reason: str = None,
        no_perms_type: str = None,
        **fields: str) -> Embed:

    if fields:

        config["fields"] = [
            {"name": f, "value": v or '`Nothing to show...`',
                "inline": (reason != None)}
            for f, v in fields.items()]

        if reason:
            config["fields"].append(
                {"name": "Reason",
                 "value": reason or "`No reason given...`",
                 "inline": True}
            )

    if no_perms_type:

        ft = config.pop('footer')

        config['footer'] = {
            'text': ft[no_perms_type]['text'],
            'icon_url': ft[no_perms_type]['icon_url']
        }

    return Embed.from_dict(config)
