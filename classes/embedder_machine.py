from typing import Optional
from discord import Embed


class EmbedderMachine:
    def __init__(self):

        self.__embed = Embed()

    def add_components(
        self,
        title: str,
        url: str,
        author_name: str,
        description: str,
        color: int,
        author_image: str,
        author_url: Optional[str],
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
        footer_url: Optional[str] = None,
        footer_text: Optional[str] = None,
    ):

        self.__embed.title = title
        self.__embed.description = description
        self.__embed.set_author(name=author_name, icon_url=author_image)
