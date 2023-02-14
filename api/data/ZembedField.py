from typing import Any, Optional


class ZembedField:
    def __init__(
        self, name: str, value: str, inline: bool = False
    ):
        self.name = name
        self.value = value
        self.inline = inline
