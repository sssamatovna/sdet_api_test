import allure
import json
import requests
from requests import Response
from src.models import EntityRequest
from src.endpoints import ApiEndpoints
from src.base_requests import BaseRequests  # Импортируем обертку

class ApiClient:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.requests = BaseRequests()  # Используем класс-обертку

    def _log_request(self, response: Response) -> None:
        try:
            allure.attach(
                f"{response.request.method} {response.request.url}",
                "Request URL",
                allure.attachment_type.TEXT,
            )
            if response.request.body:
                try:
                    request_body_json = json.dumps(
                        json.loads(response.request.body), indent=2, ensure_ascii=False
                    )
                    allure.attach(
                        request_body_json,
                        "Request Body",
                        allure.attachment_type.JSON,
                    )
                except json.JSONDecodeError:
                    allure.attach(
                        response.request.body, "Request Body (Text)", allure.attachment_type.TEXT
                    )
            allure.attach(
                f"Status Code: {response.status_code}",
                "Response Status Code",
                allure.attachment_type.TEXT,
            )
            if response.text:
                try:
                    response_body_json = json.dumps(
                        response.json(), indent=2, ensure_ascii=False
                    )
                    allure.attach(
                        response_body_json,
                        "Response Body",
                        allure.attachment_type.JSON,
                    )
                except json.JSONDecodeError:
                    allure.attach(
                        response.text, "Response Body (Text)", allure.attachment_type.TEXT
                    )
        except Exception as e:
            allure.attach(
                f"Ошибка при логировании: {e}",
                "Logging Error",
                allure.attachment_type.TEXT,
            )

    def create_entity(self, payload: EntityRequest) -> Response:
        url = f"{self.base_url}{ApiEndpoints.CREATE_ENTITY}"
        # Заменяем requests.post на self.requests.post
        response = self.requests.post(url, json=payload.model_dump())
        self._log_request(response)
        return response

    def get_entity(self, entity_id: int) -> Response:
        url = f"{self.base_url}{ApiEndpoints.get_entity_by_id(entity_id)}"
        # Заменяем requests.get на self.requests.get
        response = self.requests.get(url)
        self._log_request(response)
        return response

    def get_all_entities(self, params: dict = None) -> Response:
        url = f"{self.base_url}{ApiEndpoints.GET_ALL_ENTITIES}"
        # Заменяем requests.get на self.requests.get
        response = self.requests.get(url, params=params)
        self._log_request(response)
        return response

    def update_entity(self, entity_id: int, payload: EntityRequest) -> Response:
        url = f"{self.base_url}{ApiEndpoints.update_entity_by_id(entity_id)}"
        # Заменяем requests.patch на self.requests.patch
        response = self.requests.patch(url, json=payload.model_dump())
        self._log_request(response)
        return response

    def delete_entity(self, entity_id: int) -> Response:
        url = f"{self.base_url}{ApiEndpoints.delete_entity_by_id(entity_id)}"
        # Заменяем requests.delete на self.requests.delete
        response = self.requests.delete(url)
        self._log_request(response)
        return response