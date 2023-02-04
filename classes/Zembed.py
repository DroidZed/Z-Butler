from typing import Optional
from discord import Embed


class Zembed(Embed):
    def set_title(self, title: str):
        self.title = title
        return self

    def set_description(self, description: str):
        self.description = description
        return self

    def set_color(self, color: int):
        self.color = color
        return self

    def set_url(self, url: Optional[str]):
        self.url = url
        return self
