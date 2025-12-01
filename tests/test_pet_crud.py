from api.pet_client import PetClient


def test_create_and_get_pet(base_url, new_pet_payload):
    # создаём клиент для API
    client = PetClient(base_url)

    # 1. Создаём нового питомца
    create_resp = client.add_pet(new_pet_payload)
    assert create_resp.ok  # базовая проверка, что запрос прошёл

    created = create_resp.json()
    pet_id = created["id"]

    # 2. Проверяем, что данные сохранились корректно
    assert created["name"] == new_pet_payload["name"]
    assert created["status"] == new_pet_payload["status"]

    # 3. Получаем питомца по его id
    get_resp = client.get_pet(pet_id)
    assert get_resp.status_code == 200

    got = get_resp.json()

    # 4. Проверяем, что API вернул именно нашего питомца
    assert got["id"] == pet_id
    assert got["name"] == new_pet_payload["name"]
    assert got["status"] == new_pet_payload["status"]


def test_update_pet_status(base_url, new_pet_payload):
    client = PetClient(base_url)

    # создаём питомца
    create_resp = client.add_pet(new_pet_payload)
    assert create_resp.ok
    pet = create_resp.json()
    pet_id = pet["id"]

    # 1. Обновляем статус питомца
    pet["status"] = "sold"
    update_resp = client.update_pet(pet)
    assert update_resp.ok

    # 2. Проверяем, что статус действительно обновился
    get_resp = client.get_pet(pet_id)
    assert get_resp.status_code == 200
    got = get_resp.json()
    assert got["status"] == "sold"


def test_delete_pet(base_url, new_pet_payload):
    client = PetClient(base_url)

    # создаём питомца
    create_resp = client.add_pet(new_pet_payload)
    assert create_resp.ok
    pet_id = create_resp.json()["id"]

    # 1. Удаляем питомца — API может вернуть 200/204/404
    delete_resp = client.delete_pet(pet_id)
    assert delete_resp.status_code in (200, 204, 404)

    # 2. После удаления питомец больше не должен находиться
    get_resp = client.get_pet(pet_id)
    assert get_resp.status_code in (404, 400)


def test_find_pets_by_status_returns_created_pet(base_url, new_pet_payload):
    client = PetClient(base_url)

    # создаём питомца со статусом "available"
    create_resp = client.add_pet(new_pet_payload)
    assert create_resp.ok
    pet = create_resp.json()
    pet_id = pet["id"]

    # 1. Ищем всех питомцев со статусом "available"
    find_resp = client.find_pets_by_status("available")
    assert find_resp.status_code == 200

    pets = find_resp.json()

    # 2. Проверяем, что наш питомец присутствует в выдаче
    assert any(p.get("id") == pet_id for p in pets)


def test_get_nonexistent_pet_returns_404_or_400(base_url):
    client = PetClient(base_url)

    # запрашиваем очень большой id, которого точно нет
    resp = client.get_pet(999999999999)

    # API может вернуть 404 или 400 — обе реакции допустимы
    assert resp.status_code in (404, 400)
