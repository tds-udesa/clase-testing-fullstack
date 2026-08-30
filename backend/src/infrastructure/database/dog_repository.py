from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.dog import Dog
from src.app.repositories.dogs import DogRepository
from src.infrastructure.database.models.dog_orm import Dog as DogModel


@dataclass
class SqlAlchemyDogRepository(DogRepository):
    session: AsyncSession

    async def get_all_dogs(self) -> list[Dog]:

        query = select(DogModel)

        result = await self.session.execute(query)

        dogs = result.scalars().all()

        return [Dog(id=dog.id, url=dog.url, category=dog.category) for dog in dogs]

    async def save(self, dog: Dog) -> Dog:
        dog_to_insert = DogModel(url=dog.url, category=dog.category)
        self.session.add(dog_to_insert)

        await self.session.commit()
        await self.session.refresh(dog_to_insert)

        return Dog(
            id=dog_to_insert.id, url=dog_to_insert.url, category=dog_to_insert.category
        )
