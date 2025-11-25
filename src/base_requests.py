import requests
from requests import Response

class BaseRequests:

    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None) -> Response:
        """Отправляет GET-запрос."""
        return requests.get(url, params=params, headers=headers)

    @staticmethod
    def post(url: str, json: dict = None, data: dict = None, headers: dict = None) -> Response:
        """Отправляет POST-запрос."""
        return requests.post(url, json=json, data=data, headers=headers)

    @staticmethod
    def patch(url: str, json: dict = None, data: dict = None, headers: dict = None) -> Response:
        """Отправляет PATCH-запрос."""
        return requests.patch(url, json=json, data=data, headers=headers)

    @staticmethod
    def delete(url: str, headers: dict = None) -> Response:
        """Отправляет DELETE-запрос."""
        return requests.delete(url, headers=headers)