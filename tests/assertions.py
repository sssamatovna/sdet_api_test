from requests import Response
import allure

class Assertions:

    @staticmethod
    @allure.step("Проверка статус-кода. Ожидается: {expected_code}")
    def assert_status_code(response: Response, expected_code: int):
        actual_code = response.status_code
        assert actual_code == expected_code, \
            f"Ожидался статус-код {expected_code}, но получен {actual_code}. Ответ: {response.text}"

    @staticmethod
    @allure.step("Проверка, что ID {entity_id} присутствует в списке")
    def assert_entity_in_list(entity_id: int, entity_list: list):
        entity_ids = [e.id for e in entity_list]
        assert entity_id in entity_ids, \
            f"Сущность с ID {entity_id} не найдена в списке /getAll"

    @staticmethod
    @allure.step("Проверка, что ID {entity_id} отсутствует в списке")
    def assert_entity_not_in_list(entity_id: int, entity_list: list):
        entity_ids = [e.id for e in entity_list]
        assert entity_id not in entity_ids, \
            f"Удаленная сущность с ID {entity_id} всё ещё присутствует в списке /getAll"