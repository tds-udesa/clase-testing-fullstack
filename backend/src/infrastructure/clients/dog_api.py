import httpx

from src.app.clients.dog_api import DogClient


class DogAPIClient(DogClient):
    base_url = "https://dog.ceo/api/"

    async def fetch_random_dog(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/breeds/image/random")
            response.raise_for_status()

            return response.json().get("message")
