from typing import Optional
from discord import Guild

server_image = "https://cdn.discordapp.com/attachments/1012475750940672080/1071067387144712202/7ccc95853e9c7c2b09930d55b1d795aa.png"


def get_server_image(g: Optional[Guild]) -> Optional[str]:
    return g.icon.url if g and g.icon else None
