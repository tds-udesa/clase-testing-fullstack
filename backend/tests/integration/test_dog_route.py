import pytest

from unittest.mock import patch
from fastapi.testclient import TestClient
from src.api.dependencies import get_db
from src.api.app import app
from src.api.schemas.dogs import SaveRequest, SavedDogImage, RandomDogImage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class TestDogRoute:

    @pytest.fixture(scope="class")
    @classmethod
    def test_engine(cls, tmp_path_factory):

        tmp_db = tmp_path_factory.mktemp("data") / "test.db"
        url = f"sqlite+aiosqlite:///{tmp_db}".replace('\\', '/')

        return create_async_engine(url)

    @pytest.fixture(scope="class")
    @classmethod
    def get_db_override(cls, test_engine):

        AsyncLocalSession = async_sessionmaker(test_engine)

        async def override_dependency():
            async with AsyncLocalSession() as db:
                yield db

        return override_dependency

    @pytest.fixture(scope="class")
    @classmethod
    def client(cls, get_db_override, test_engine):
        app.dependency_overrides[get_db] = get_db_override

        with patch("src.api.app.engine", test_engine), TestClient(app, root_path=app.root_path) as test_client:
            yield test_client

        app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_get_random_dog(self, client: TestClient):
        response = client.get("/dogs/random")

        assert response.status_code == 200
        data = RandomDogImage(**response.json())

        assert data.url is not None

    @pytest.mark.integration
    def test_save_new_dog(self, client: TestClient):
        payload = SaveRequest(url="https://images.dog.ceo/breeds/beegle/n02108422_251.jpg")
        response = client.post("/dogs/save", json=payload.model_dump())

        data = SavedDogImage(**response.json())

        assert response.status_code == 201
        assert data.id > 0
        assert data.category == "beegle"
        assert data.url == "https://images.dog.ceo/breeds/beegle/n02108422_251.jpg"


    @pytest.mark.integration
    def test_get_my_dogs(self, client: TestClient):

        payloads = [
            SaveRequest(url="https://images.dog.ceo/breeds/beegle/1.jpg"),
            SaveRequest(url="https://images.dog.ceo/breeds/beegle/2.jpg"),
            SaveRequest(url="https://images.dog.ceo/breeds/beegle/3.jpg"),

            ]
        for payload in payloads:
            response = client.post("/dogs/save", json=payload.model_dump())
            assert response.status_code == 201

        response = client.get("/dogs/my-dogs")


        assert response.status_code == 200
        data = [SavedDogImage(**i) for i in response.json()]
        assert all(d.url is not None for d in data)
        assert len(data) == len(payloads)
