from abc import ABC, abstractmethod


class DogClient(ABC):
    @abstractmethod
    async def fetch_random_dog(self) -> str:
        pass
