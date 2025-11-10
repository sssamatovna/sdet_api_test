import pytest
import os
from dotenv import load_dotenv
from src.api_client import ApiClient
import data as test_data  # <-- Обновленный импорт (Правка 5)
from tests.assertions import Assertions  # <-- Импорт ассертов (Правка 4)

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """
    Фикстура, которая читает и возвращает базовый URL для API-сервиса.
    """
    url = os.getenv("API_HOST")
    if not url:
        pytest.fail("Переменная окружения API_HOST не задана в .env файле")
    return f"{url}/api"


@pytest.fixture(scope="session")
def api_client(base_url):
    """
    Фикстура, которая создает и настраивает экземпляр API-клиента.
    """
    client = ApiClient(base_url=base_url)
    return client


@pytest.fixture
def created_entity(api_client: ApiClient):
    """
    Фикстура для создания и последующей очистки одной сущности.
    """
    payload = test_data.default_entity()
    create_response = api_client.create_entity(payload)

    # Используем кастомный ассерт
    Assertions.assert_status_code(create_response, 200)

    entity_id = int(create_response.text)

    yield entity_id, payload

    # Teardown
    api_client.delete_entity(entity_id)


@pytest.fixture
def created_entities_for_filter_test(api_client):
    """
    Фикстура для теста фильтрации.
    """
    entities_to_delete = []

    verified_payload = test_data.verified_entity()
    unverified_payload = test_data.unverified_entity()

    create_verified_res = api_client.create_entity(verified_payload)
    verified_id = int(create_verified_res.text)
    entities_to_delete.append(verified_id)

    create_unverified_res = api_client.create_entity(unverified_payload)
    unverified_id = int(create_unverified_res.text)
    entities_to_delete.append(unverified_id)

    yield {
        "verified_id": verified_id,
        "unverified_id": unverified_id,
        "unverified_title": unverified_payload.title,
    }

    for entity_id in entities_to_delete:
        api_client.delete_entity(entity_id)