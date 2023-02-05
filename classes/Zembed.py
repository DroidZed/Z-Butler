from typing import Optional
from discord import Embed

from config.colors import BOT_COLOR


class Zembed(Embed):
    def set_title(self, title: Optional[str]):
        if title:
            self.title = title
        return self

    def set_description(self, description: Optional[str]):
        if description:
            self.description = description
        return self

    def set_color(self, color: Optional[int]):
        self.color = color or BOT_COLOR
        return self

    def set_url(self, url: Optional[str]):
        if url:
            self.url = url
        return self

    def add_thumbnail(self, thumbnail_url: Optional[str]):
        if thumbnail_url:
            self.set_thumbnail(url=thumbnail_url)
        return self

    def attach_image(self, image_url: Optional[str]):
        if image_url:
            self.set_image(url=image_url)
        return self
