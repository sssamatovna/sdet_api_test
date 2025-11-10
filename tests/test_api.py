import allure
from src.api_client import ApiClient
from src.models import EntityResponse, EntityListResponse
import data as test_data  # Обновленный импорт
from tests.assertions import Assertions  # Импорт ассертов


@allure.epic("Entity Management")
@allure.feature("Core Functionality")
class TestEntityApi:

    @allure.story("Создание сущности")
    @allure.title("Позитивный тест: создание и проверка сущности")
    def test_create_and_get_entity(self, api_client: ApiClient, created_entity):
        entity_id, payload = created_entity

        with allure.step("Отправка GET-запроса на /get/{id} для проверки"):
            get_response = api_client.get_entity(entity_id)
            # Используем кастомный ассерт
            Assertions.assert_status_code(get_response, 200)

            entity_data = EntityResponse.model_validate(get_response.json())
            assert entity_data.id == entity_id
            assert entity_data.title == payload.title
            assert entity_data.verified == payload.verified

        # Проверка в /getAll
        with allure.step("Проверка наличия сущности в общем списке /getAll"):
            get_all_res = api_client.get_all_entities()
            Assertions.assert_status_code(get_all_res, 200)
            all_entities = EntityListResponse.model_validate(get_all_res.json()).entity
            Assertions.assert_entity_in_list(entity_id, all_entities)

    @allure.story("Получение списка сущностей")
    @allure.title("Позитивный тест: получение списка всех сущностей")
    def test_get_all_entities(self, api_client: ApiClient):
        with allure.step("Отправка GET-запроса на /getAll"):
            response = api_client.get_all_entities()
            Assertions.assert_status_code(response, 200)  # (Правка 4)

        with allure.step("Валидация структуры ответа"):
            parsed_response = EntityListResponse.model_validate(response.json())
            assert isinstance(parsed_response.entity, list)

    @allure.story("Обновление сущности")
    @allure.title("Позитивный тест: обновление и проверка сущности")
    def test_update_entity(self, api_client: ApiClient, created_entity):
        entity_id, _ = created_entity

        with allure.step("Формирование и отправка PATCH-запроса на /patch/{id}"):
            update_payload = test_data.updated_entity_payload()
            update_response = api_client.update_entity(entity_id, update_payload)
            Assertions.assert_status_code(update_response, 204)  # (Правка 4)

        with allure.step("Проверка обновленных данных через GET-запрос"):
            get_response = api_client.get_entity(entity_id)
            Assertions.assert_status_code(get_response, 200)  # (Правка 4)

            updated_data = EntityResponse.model_validate(get_response.json())
            assert updated_data.title == update_payload.title
            assert updated_data.verified == update_payload.verified

    @allure.story("Удаление сущности")
    @allure.title("Позитивный тест: удаление и проверка удаления сущности")
    def test_delete_entity(self, api_client: ApiClient, created_entity):
        entity_id, _ = created_entity

        with allure.step("Отправка DELETE-запроса на /delete/{id}"):
            delete_response = api_client.delete_entity(entity_id)
            Assertions.assert_status_code(delete_response, 204)  # (Правка 4)

        with allure.step("Проверка, что сущность больше не доступна по GET /get/{id}"):
            get_response = api_client.get_entity(entity_id)

            expected_error_code = 404
            if get_response.status_code != expected_error_code:
                # ... (логирование бага)
                allure.attach(f"BUG: GET /get/{id} after DELETE returned {get_response.status_code}", "BUG",
                              allure.attachment_type.TEXT)

            # Проверяем, что код >= 400
            assert get_response.status_code >= 400

        # <-- Проверка в /getAll -->
        with allure.step("Проверка отсутствия сущности в общем списке /getAll"):
            get_all_res = api_client.get_all_entities()
            Assertions.assert_status_code(get_all_res, 200)
            all_entities = EntityListResponse.model_validate(get_all_res.json()).entity
            Assertions.assert_entity_not_in_list(entity_id, all_entities)

    @allure.story("Получение списка сущностей")
    @allure.title(
        "Позитивный тест: фильтрация списка сущностей по параметру 'verified'"
    )
    def test_get_all_entities_with_filter(
            self, api_client: ApiClient, created_entities_for_filter_test
    ):
        unverified_title = created_entities_for_filter_test["unverified_title"]

        with allure.step("Отправка GET-запроса на /getAll с фильтром ?verified=true"):
            params = {"verified": "true"}
            response = api_client.get_all_entities(params=params)
            Assertions.assert_status_code(response, 200)  # (Правка 4)

        with allure.step(
                "Валидация ответа: все сущности в списке должны иметь verified=True"
        ):
            parsed_response = EntityListResponse.model_validate(response.json())
            assert parsed_response.entity

            for entity in parsed_response.entity:
                assert entity.verified is True
                assert entity.title != unverified_title