from dataclasses import dataclass

@dataclass(repr=True)
class Sneep:
    _id: str
    content: str
    author_handle: str