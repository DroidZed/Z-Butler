from discord import Embed

def create_config_dictionary(name,value,inline):
    return {"name": name,
            "value": value,
            "inline":inline}


class EmbedFactory:
    @staticmethod
    def create_config(**kwargs):
        return {k: v for k, v in kwargs.items()}

    @staticmethod
    def create_admin_embed(config: dict, reason: str | None = None, cfg_type: str | None = None, **fields: dict) -> Embed:
        cfg = ["mod", "ping", "mute", "strike", "ban"]

        # default fields
        if fields:
            config["fields"] = [
                # adding each dictionary to the list 
                create_config_dictionary(f, v or "`Nothing to show...`",cfg_type in cfg)
                for f, v in fields.items() 
            ]
            # reason if it exists
            if reason:
                config["fields"].append(
                    create_config_dictionary("Reason",reason or "`No reason given...`",True)
                )
        if cfg_type and cfg_type in {"mod, stats"}:
            # restructuring the footer field
            footer = config.pop("footer")

            config["footer"] = {"text": footer[cfg_type]["text"], "icon_url": footer[cfg_type]["icon_url"]}

        return Embed.from_dict(config)

    @staticmethod
    def create_embed(config: dict, cfg_type: str | None = None, **fields) -> Embed:
        cfg = ["mod", "ping", "mute", "strike", "ban"]
        if fields:

            config["fields"] = [
                create_config_dictionary(f,v or "`Nothing to show...`",cfg_type in cfg)
                for f, v in fields.items()
            ]

        if cfg_type and cfg_type in {"mod, stats"}:
            footer = config.pop("footer")
            config["footer"] = {"text": footer[cfg_type]["text"], "icon_url": footer[cfg_type]["icon_url"]}
        return Embed.from_dict(config)
