from typing import Optional
from api.data.ZembedField import ZembedField
from api.data.Zembed import Zembed

from classes.embedder_machine import EmbedderMachine


def generate_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    color: Optional[int] = None,
    url: Optional[str] = None,
    thumbnail_url: Optional[str] = None,
    image_url: Optional[str] = None,
    footer_icon: Optional[str] = None,
    footer_text: Optional[str] = None,
    rem_img=False,
    *fields: ZembedField,
) -> Zembed:

    machine = EmbedderMachine()

    machine.set_embed_components(
        title,
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
