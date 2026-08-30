async def get_dog_api_client():
    from src.infrastructure import DogAPIClient

    yield DogAPIClient()


async def get_db():
    from src.infrastructure.database.session import AsyncLocalSession

    async with AsyncLocalSession() as db:
        yield db
