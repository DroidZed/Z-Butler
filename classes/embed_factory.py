from discord import Embed


class EmbedFactory:
    @staticmethod
    def create_config(**kwargs):
        return {k: v for k, v in kwargs.items()}

    @staticmethod
    def create_admin_embed(config: dict, reason: str | None = None, cfg_type: str | None = None, **fields: dict) -> Embed:

        cfg = ["mod", "ping", "mute", "strike", "ban"]

        if fields:

            config["fields"] = [
                {
                    "name": f,
                    "value": v or "`Nothing to show...`",
                    "inline": cfg_type in cfg,
                }
                for f, v in fields.items()
            ]

            if reason:
                config["fields"].append(
                    {
                        "name": "Reason",
                        "value": reason or "`No reason given...`",
                        "inline": True,
                    }
                )

        if cfg_type and cfg_type in {"mod, stats"}:
            footer = config.pop("footer")

            config["footer"] = {"text": footer[cfg_type]["text"], "icon_url": footer[cfg_type]["icon_url"]}

        return Embed.from_dict(config)

    @staticmethod
    def create_embed(config: dict, cfg_type: str | None = None, **fields: dict) -> Embed:

        cfg = ["mod", "ping", "mute", "strike", "ban"]

        if fields:

            config["fields"] = [
                {
                    "name": f,
                    "value": v or "`Nothing to show...`",
                    "inline": cfg_type in cfg,
                }
                for f, v in fields.items()
            ]

        if cfg_type and cfg_type in {"mod, stats"}:
            footer = config.pop("footer")

            config["footer"] = {"text": footer[cfg_type]["text"], "icon_url": footer[cfg_type]["icon_url"]}

        return Embed.from_dict(config)
