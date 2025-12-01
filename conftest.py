import random
import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://petstore.swagger.io/v2"


def _random_id() -> int:
    return random.randint(1_000_000, 9_999_999)


@pytest.fixture
def new_pet_payload() -> dict:
    pet_id = _random_id()
    return {
        "id": pet_id,
        "name": f"test-pet-{pet_id}",
        "photoUrls": ["https://example.com/photo.png"],
        "status": "available",
    }