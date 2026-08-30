from abc import ABC, abstractmethod

from src.app.models.dog import Dog


class DogRepository(ABC):
    @abstractmethod
    async def get_all_dogs(self) -> list[Dog]:
        pass

    @abstractmethod
    async def save(self, dog: Dog) -> Dog:
        pass
