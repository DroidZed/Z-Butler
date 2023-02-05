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
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[int] = None,
        url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
    ):

        self.__embed.set_title(title).set_description(
            description
        ).set_author(
            name="The Z Butler",
            icon_url="https://cdn.discordapp.com/avatars/759844892443672586"
            "/bb7df4730c048faacd8db6dd99291cdb.jpg",
        ).set_color(
            color
        ).set_url(
            url
        ).add_thumbnail(
            thumbnail_url
        ).attach_image(
            image_url
        )

        return self

    def add_fields(self, *fields: ZembedField):

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

    def remove_image(self):
        self.__embed.remove_image()
        return self