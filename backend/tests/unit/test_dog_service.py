from unittest.mock import AsyncMock
import pytest
from src.app.repositories.dogs import DogRepository
from src.app.clients.dog_api import DogClient
from src.app.models.dog import Dog
from src.app.services import DogService
from src.infrastructure.clients.dog_api import DogAPIClient


class TestCorrectDogService:

    @pytest.mark.unit
    @pytest.mark.parametrize("test_input,expected", [
        ("https://images.dog.ceo/breeds/mastiff-bull/n02108422_251.jpg", "mastiff-bull"),
        ("https://images.dog.ceo/breeds/pit-bull/n02108422_251.jpg", "pit-bull"),
        ("https://images.dog.ceo/breeds/beegle/n02108422_251.jpg", "beegle"),
    ])
    async def test_dog_service_extract_category_from_url(self, test_input, expected):
        # Arrange
        service = DogService()
        # Act
        category = service._extract_category(test_input)

        # Assert
        assert category == expected

    @pytest.mark.unit
    async def test_dog_service_raise_exception_when_invalid_url(self):
        # Arrange
        service = DogService()
        invalid_url = "https://images.dog.ceo/breeds/dogs"

        # Act& Assert
        with pytest.raises(ValueError) as exception:
            service._extract_category(invalid_url)
        assert str(exception.value) == "Invalid URL"

    @pytest.mark.unit
    async def test_get_dog_fetch_and_returns_new_dog_url(self):
        # Arrange
        mock_client = AsyncMock(spec=DogClient)
        mock_client.fetch_random_dog.return_value = "https://images.dog.ceo/breeds/beegle/n02108422_251.jpg"

        service = DogService(dog_api_client=mock_client)

        # Act
        url = await service.get_dog()

        # Assert
        mock_client.fetch_random_dog.assert_awaited_once()
        assert url == "https://images.dog.ceo/breeds/beegle/n02108422_251.jpg"

    @pytest.mark.unit
    async def test_get_dog_raise_exception_when_client_is_not_initialized(self):
        # Arrange
        service = DogService()

        # Act & Assert
        with pytest.raises(ValueError) as exception:
            await service.get_dog()
        assert str(exception.value) == "Dog API client is not initialized"

    @pytest.mark.unit
    async def test_save_dog_save_in_db_and_returns_saved_dog(self):
        # Arrange
        mock_repo = AsyncMock(spec=DogRepository)
        mock_repo.save.return_value = Dog(
            id= 1,
            category="pit-bull",
            url ="https://images.dog.ceo/breeds/pit-bull/n02108422_251.jpg"
        )

        service = DogService(dog_repository=mock_repo)

        # Act
        saved_dog = await service.save_dog(url="https://images.dog.ceo/breeds/pit-bull/n02108422_251.jpg")

        # Assert
        mock_repo.save.assert_awaited_once()
        assert saved_dog.id == 1
        assert saved_dog.category == "pit-bull"
        assert saved_dog.url == "https://images.dog.ceo/breeds/pit-bull/n02108422_251.jpg"

    @pytest.mark.unit
    async def test_save_dog_raise_exception_when_repository_is_not_initialized(self):
        # Arrange
        service = DogService()

        # Act & Assert
        with pytest.raises(ValueError) as exception:
            await service.save_dog(url="https://images.dog.ceo/breeds/pit-bull/n02108422_251.jpg")
        assert str(exception.value) == "Dog repository is not initialized"

class TestIncorrectDogService:
    @pytest.mark.unit
    async def test_incorrect_dog_service_extract_category_from_url(self):
        # Arrange
        service = DogService()
        url1 = "https://images.dog.ceo/breeds/mastiff-bull/n02108422_251.jpg"
        url2 = "https://images.dog.ceo/breeds/pit-bull/n02108422_251.jpg"
        url3 = "https://images.dog.ceo/breeds/beegle/n02108422_251.jpg"
        url4 = "https://images.dog.ceo/breeds/mastiff-bull/n02108422_251.jpg"

        # Act
        category = service._extract_category(url1)
        category2 = service._extract_category(url=url2)
        category3 = service._extract_category(url3)
        category4 = service._extract_category(url4)


        # Assert
        assert category == "mastiff-bull"
        assert category2 == "pit-bull"
        assert category3 == "beegle"
        assert category4 == "mastiff-bull"

    @pytest.mark.unit
    async def test_get_dog_with_no_mock(self):
        # Arrange
        service = DogService(dog_api_client=DogAPIClient())

        # Act
        url = await service.get_dog()

        # Assert
        assert url is not None

    @pytest.mark.unit
    async def test_dog_2(self):
        # Arrange
        mock_repo = AsyncMock(spec=DogRepository)
        mock_repo.get_all_dogs.return_value = [
            Dog(id=1, category="beegle", url="https://images.dog.ceo/breeds/beegle/1.jpg")
        ]
        service = DogService(dog_repository=mock_repo)

        # Act
        dogs = await service.get_all_dogs()

        # Assert
        assert dogs

    @pytest.mark.unit
    async def test_save_dog_no_assertion(self):
        # Arrange
        mock_repo = AsyncMock(spec=DogRepository)
        mock_repo.save.return_value = Dog(
            id=1,
            category="pit-bull",
            url="https://images.dog.ceo/breeds/pit-bull/n02108422_251.jpg"
        )
        service = DogService(dog_repository=mock_repo)

        # Act
        await service.save_dog(url="https://images.dog.ceo/breeds/pit-bull/n02108422_251.jpg")

    @pytest.mark.unit
    async def test_get_all_dogs_error_handling(self):
        # Arrange
        mock_repo = AsyncMock(spec=DogRepository)
        mock_repo.get_all_dogs.side_effect = ValueError("Dog repository is not initialized")
        service = DogService(dog_repository=mock_repo)

        # Act & Assert
        try:
            await service.get_all_dogs()
        except Exception:
            pass
