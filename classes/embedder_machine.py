from typing import Optional

from classes.Zembed import Zembed
from classes.ZembedField import ZembedField


class EmbedderMachine:
    def __init__(self):

        self.__embed = Zembed()

    @property
    def embed(self):
        return self.__embed

    def set_embed_components(
        self,
        title: str,
        color: int,
        description: str,
        author_name: str,
        author_image: str,
        url: Optional[str] = None,
        author_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
    ):

        self.__embed.set_title(title).set_description(
            description
        ).set_author(
            name=author_name,
            icon_url=author_image,
            url=author_url,
        ).set_color(
            color
        ).set_url(
            url
        ).set_thumbnail(
            url=thumbnail_url
        ).set_image(
            url=image_url
        )

        return self

    def add_fields(self, fields: list[ZembedField]):

        for field in fields:
            self.__embed.add_field(
                name=field.name,
                value=field.value,
                inline=field.inline,
            )

        return self

    def add_footer(
        self, footer_icon: str, footer_text: str
    ):

        self.__embed.set_footer(
            text=footer_text, icon_url=footer_icon
        )

        return self
