from dataclasses import dataclass

@dataclass(repr=True)
class CatFact:
    fact: str
    length: int


@dataclass(repr=True)
class DocPicture:
    message: str
    status: str