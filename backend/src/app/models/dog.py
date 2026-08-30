from dataclasses import dataclass


@dataclass
class Dog:
    url: str
    category: str
    id: int | None = None
