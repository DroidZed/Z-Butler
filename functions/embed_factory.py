from discord import Embed


def create_embed(
        config: dict,
        reason: str = None,
        cfg_type: str = None,
        **fields: str) -> Embed:
    cfg = ['mod', 'stats', 'ping', 'mute', 'strike', 'ban']

    if fields:

        config["fields"] = [
            {
                "name": f,
                "value": v or '`Nothing to show...`',
                "inline": cfg_type in cfg,
            }
            for f, v in fields.items()
        ]

        if reason:
            config["fields"].append(
                {
                    "name": "Reason",
                    "value": reason or "`No reason given...`",
                    "inline": True
                }
            )

    if cfg_type and cfg_type not in cfg[0:3]:
        ft = config.pop('footer')

        config['footer'] = {
            'text': ft[cfg_type]['text'],
            'icon_url': ft[cfg_type]['icon_url']
        }

    return Embed.from_dict(config)
