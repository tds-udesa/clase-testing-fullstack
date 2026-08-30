from pydantic import BaseModel


class RandomDogImage(BaseModel):
    url: str


class SavedDogImage(BaseModel):
    id: int
    category: str
    url: str


class SaveRequest(BaseModel):
    url: str
