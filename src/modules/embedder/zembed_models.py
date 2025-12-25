from typing import Optional, Any
from dataclasses import dataclass
from discord import Embed

from utils import Env


@dataclass
class ZembedField:
    name: str
    value: Any
    inline: bool = False


class Zembed(Embed):
    def set_title(self, title: Optional[str]):
        if title:
            self.title = title

    def set_description(self, description: Optional[str]):
        if description:
            self.description = description

    def set_color(self, color: Optional[int]):
        self.color = color or Env.BOT_COLOR

    def set_url(self, url: Optional[str]):
        if url:
            self.url = url

    def add_thumbnail(self, thumbnail_url: Optional[str]):
        if thumbnail_url:
            self.set_thumbnail(url=thumbnail_url)

    def attach_image(self, image_url: Optional[str]):
        if image_url:
            self.set_image(url=image_url)
