import allure
from src.api_client import ApiClient
from src.models import EntityResponse, EntityListResponse
from tests import test_data


@allure.epic("Entity Management")
@allure.feature("Core Functionality")
class TestEntityApi:

    @allure.story("Создание сущности")
    @allure.title("Позитивный тест: создание и проверка сущности")
    def test_create_and_get_entity(self, api_client: ApiClient, created_entity):
        entity_id, payload = created_entity

        with allure.step("Отправка GET-запроса на /get/{id} для проверки"):
            get_response = api_client.get_entity(entity_id)

            assert (
                    get_response.status_code == 200
            ), f"Ожидался статус-код 200, но получен {get_response.status_code}. Ответ: {get_response.text}"

            entity_data = EntityResponse.model_validate(get_response.json())
            assert (
                    entity_data.id == entity_id
            ), f"ID полученной сущности не совпадает. Ожидался {entity_id}, получен {entity_data.id}"
            assert (
                    entity_data.title == payload.title
            ), f"Title сущности не совпадает. Ожидался '{payload.title}', получен '{entity_data.title}'"
            assert (
                    entity_data.verified == payload.verified
            ), "Статус verified не совпадает с отправленным payload"

    @allure.story("Получение списка сущностей")
    @allure.title("Позитивный тест: получение списка всех сущностей")
    def test_get_all_entities(self, api_client: ApiClient):
        with allure.step("Отправка GET-запроса на /getAll"):
            response = api_client.get_all_entities()
            assert (
                    response.status_code == 200
            ), f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"

        with allure.step("Валидация структуры ответа"):
            parsed_response = EntityListResponse.model_validate(response.json())
            assert isinstance(
                parsed_response.entity, list
            ), "Ключ 'entity' должен содержать список"

    @allure.story("Обновление сущности")
    @allure.title("Позитивный тест: обновление и проверка сущности")
    def test_update_entity(self, api_client: ApiClient, created_entity):
        entity_id, _ = created_entity

        with allure.step("Формирование и отправка PATCH-запроса на /patch/{id}"):
            update_payload = test_data.updated_entity_payload()
            update_response = api_client.update_entity(entity_id, update_payload)
            assert (
                    update_response.status_code == 204
            ), f"Ожидался статус-код 204 после обновления, но получен {update_response.status_code}. Ответ: {update_response.text}"

        with allure.step("Проверка обновленных данных через GET-запрос"):
            get_response = api_client.get_entity(entity_id)
            assert (
                    get_response.status_code == 200
            ), f"Не удалось получить сущность после обновления. Статус: {get_response.status_code}"

            updated_data = EntityResponse.model_validate(get_response.json())
            assert (
                    updated_data.title == update_payload.title
            ), f"Title не обновился. Ожидался '{update_payload.title}', получен '{updated_data.title}'"
            assert (
                    updated_data.verified == update_payload.verified
            ), f"Статус verified не обновился. Ожидался {update_payload.verified}, получен {updated_data.verified}"

    @allure.story("Удаление сущности")
    @allure.title("Позитивный тест: удаление и проверка удаления сущности")
    def test_delete_entity(self, api_client: ApiClient, created_entity):
        entity_id, _ = created_entity

        with allure.step("Отправка DELETE-запроса на /delete/{id}"):
            delete_response = api_client.delete_entity(entity_id)
            assert (
                    delete_response.status_code == 204
            ), f"Ожидался статус-код 204 после удаления, но получен {delete_response.status_code}. Ответ: {delete_response.text}"

        with allure.step("Проверка, что сущность больше не доступна по GET"):
            get_response = api_client.get_entity(entity_id)


            expected_error_code = 404
            if get_response.status_code != expected_error_code:
                bug_message = (
                    f"Обнаружен баг: GET после DELETE для ID {entity_id} "
                    f"возвращает {get_response.status_code} "
                    f"вместо ожидаемого {expected_error_code}. "
                    f"Response: {get_response.text}"
                )
                allure.attach(
                    bug_message,
                    name="BUG: Wrong status code after deletion",
                    attachment_type=allure.attachment_type.TEXT,
                )

            assert (
                    get_response.status_code >= 400
            ), f"Ожидался код ошибки (4xx-5xx), но получен {get_response.status_code}. Сущность всё ещё доступна!"

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
            assert (
                    response.status_code == 200
            ), f"Запрос с фильтром вернул неверный статус-код: {response.status_code}"

        with allure.step(
                "Валидация ответа: все сущности в списке должны иметь verified=True"
        ):
            parsed_response = EntityListResponse.model_validate(response.json())

            assert (
                parsed_response.entity
            ), "Список отфильтрованных сущностей не должен быть пустым (verified=True)"

            for entity in parsed_response.entity:
                assert (
                        entity.verified is True
                ), f"Найдена сущность '{entity.title}' с verified=False при фильтре verified=true"
                assert (
                        entity.title != unverified_title
                ), f"В отфильтрованном списке найдена сущность '{unverified_title}', которая не должна была туда попасть"