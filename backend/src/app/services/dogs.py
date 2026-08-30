from src.app.clients.dog_api import DogClient
from src.app.models.dog import Dog
from src.app.repositories.dogs import DogRepository


class DogService:
    def __init__(
        self,
        dog_api_client: DogClient | None = None,
        dog_repository: DogRepository | None = None,
    ):
        self.dog_api_client = dog_api_client
        self.dog_repository = dog_repository

    def _extract_category(self, url: str) -> str:
        # valid url format: https://images.dog.ceo/breeds/{category}/{image_name}.jpg
        if (
            not url.startswith("https://images.dog.ceo/breeds/")
            or len(url.split("/")) == 5
        ):
            raise ValueError("Invalid URL")

        if not url.endswith(".jpg"):
            raise ValueError("Invalid URL")

        return url.split("/")[-2]

    async def save_dog(self, url: str) -> Dog:
        category = self._extract_category(url)
        dog = Dog(url=url, category=category)

        if not self.dog_repository:
            raise ValueError("Dog repository is not initialized")

        saved_dog_image = await self.dog_repository.save(dog)
        return saved_dog_image

    async def get_dog(self) -> str:
        if not self.dog_api_client:
            raise ValueError("Dog API client is not initialized")
        return await self.dog_api_client.fetch_random_dog()

    async def get_all_dogs(self) -> list[Dog]:
        if not self.dog_repository:
            raise ValueError("Dog repository is not initialized")
        return await self.dog_repository.get_all_dogs()
