from typing import Optional

from .zembed_models import Zembed, ZembedField
from utils import Env


class EmbedderMachine:
    def __init__(self):
        self.__embed = Zembed()

    @property
    def embed(self):
        return self.__embed

    def set_embed_components(
        self,
        title: Optional[str] = None,
        author_name: Optional[str] = None,
        author_icon: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[int] = None,
        url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
    ):
        self.__embed.set_title(title)
        self.__embed.set_description(description)
        self.__embed.set_author(
            name=author_name or "The Z Butler",
            icon_url=author_icon
            or "https://cdn.discordapp.com/avatars/759844892443672586/bb7df4730c048faacd8db6dd99291cdb.jpg"
        )
        self.__embed.set_color(color or Env.BOT_COLOR)
        self.__embed.set_url(url)
        self.__embed.add_thumbnail(thumbnail_url)
        self.__embed.attach_image(image_url)

    def add_fields(self, *fields: ZembedField):
        for field in fields:
            self.__embed.add_field(
                name=field.name,
                value=field.value,
                inline=field.inline,
            )

    def add_footer(
        self, footer_icon: str, footer_text: str
    ):
        self.__embed.set_footer(
            text=footer_text, icon_url=footer_icon
        )

    def remove_image(self):
        self.__embed.remove_image()


def generate_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    color: Optional[int] = None,
    author_name: Optional[str] = None,
    author_icon: Optional[str] = None,
    url: Optional[str] = None,
    thumbnail_url: Optional[str] = None,
    image_url: Optional[str] = None,
    footer_icon: Optional[str] = None,
    footer_text: Optional[str] = None,
    rem_img: bool = False,
    *fields: ZembedField,
) -> Zembed:
    machine = EmbedderMachine()

    machine.set_embed_components(
        title,
        author_name,
        author_icon,
        description,
        color,
        url,
        thumbnail_url,
        image_url,
    )

    if footer_icon and footer_text:
        machine.add_footer(footer_icon, footer_text)

    machine.add_fields(*fields)

    if rem_img:
        machine.remove_image

    return machine.embed
