from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db, get_dog_api_client
from src.api.schemas.dogs import RandomDogImage, SavedDogImage, SaveRequest
from src.app.clients import DogClient
from src.app.services import DogService
from src.infrastructure.database.dog_repository import SqlAlchemyDogRepository

router = APIRouter()


@router.get(
    path="/random",
    status_code=status.HTTP_200_OK,
    summary="Get a random dog image",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "content": {
                "application/json": {"example": {"url": "https://random.dog/woof.jpg"}}
            },
        }
    },
)
async def get_dog(
    dog_client: Annotated[DogClient, Depends(get_dog_api_client)],
) -> RandomDogImage:
    """
    Get a random dog image.

    Args:
        dog_client (DogClient): The dog API client dependency.

    Returns:
        RandomDogImage: The random dog image.
    """
    try:
        dog_service = DogService(dog_api_client=dog_client)
        dog_image_url: str = await dog_service.get_dog()

        return RandomDogImage(url=dog_image_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    path="/my-dogs",
    status_code=status.HTTP_200_OK,
    summary="Get my saved dog images",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "category": "beegle",
                            "url": "https://random.dog/woof.jpg",
                        }
                    ]
                }
            },
        }
    },
)
async def get_my_dogs(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> list[SavedDogImage]:
    """
    Get my saved dog images.

    Args:
        session (AsyncSession): The database session dependency.

    Returns:
        list[SavedDogImage]: The list of saved dog images.
    """
    try:
        dog_repository = SqlAlchemyDogRepository(session=session)
        dog_service = DogService(dog_repository=dog_repository)

        saved_dogs = await dog_service.get_all_dogs()
        return [SavedDogImage(**dog.__dict__) for dog in saved_dogs]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    path="/save",
    status_code=status.HTTP_201_CREATED,
    summary="Save a dog's image",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "category": "beegle",
                        "url": "https://random.dog/woof.jpg",
                    }
                }
            },
        }
    },
)
async def save_dog(
    save_request: SaveRequest, session: Annotated[AsyncSession, Depends(get_db)]
) -> SavedDogImage:
    """
    Save a dog's image.

    Args:
        save_request (SaveRequest): The save request containing the dog image URL.
        session (AsyncSession): The database session dependency.

    Returns:
        SavedDogImage: The saved dog image.
    """
    try:
        dog_repository = SqlAlchemyDogRepository(session=session)
        dog_service = DogService(dog_repository=dog_repository)

        saved_dog = await dog_service.save_dog(url=save_request.url)

        saved_dog_image = SavedDogImage(**saved_dog.__dict__)
        return saved_dog_image
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
