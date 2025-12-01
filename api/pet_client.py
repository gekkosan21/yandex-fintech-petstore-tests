import requests


class PetClient:
    def __init__(self, base_url: str):
        # Удаляем завершающий слэш, чтобы корректно формировать пути
        self.base_url = base_url.rstrip("/")

    def add_pet(self, pet: dict):
        """
        POST /pet - создаем нового питомца в системе.
        """
        url = f"{self.base_url}/pet"
        return requests.post(url, json=pet)

    def get_pet(self, pet_id: int):
        """
        GET /pet/{petId} - возвращаем данные питомца по его ID.
        """
        url = f"{self.base_url}/pet/{pet_id}"
        return requests.get(url)

    def update_pet(self, pet: dict):
        """
        PUT /pet - обновляем существующего питомца. В API обновление выполняется полным объектом в теле запроса.
        """
        url = f"{self.base_url}/pet"
        return requests.put(url, json=pet)

    def delete_pet(self, pet_id: int):
        """
        DELETE /pet/{petId} - удаляем питомца по ID.
        """
        url = f"{self.base_url}/pet/{pet_id}"
        return requests.delete(url)

    def find_pets_by_status(self, status: str):
        """
        GET /pet/findByStatus - ищем питомцев по статусу (available / pending / sold). Использует query-параметр ?status=...
        """
        url = f"{self.base_url}/pet/findByStatus"
        return requests.get(url, params={"status": status})
