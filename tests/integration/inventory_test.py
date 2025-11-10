import uuid

import pytest

from src.inventory.inventory_dao import InventoryDAO, CategoryDAO
from tests.inventory_utils import CATEGORY_1, ITEM_1


@pytest.mark.inventory
class TestInventoryService:
    """ Тесты эндпоинтов сервиса инвентаря """

    """
    /new/category +
        тест 1: корректное создание категории
        тест 2: создание уже существующей категории
        тест 3: создание категории от обычного пользователя
    /new/item +
        тест 4: корректное добавление элемента
        тест 5: добавление уже существующего элемента
        тест 6: добавление от обычного пользователя
        тест 7: добавление с несуществующей категорией
        тест 8: добавление с некорректным количеством
    /list +
        тест 9: корректное получение списка
        тест 10: получение списка с некорректной страницей
        тест 11: корректное получение списка с фильтрами
        тест 12: получение списка с несуществующим фильтром
        тест 13: получение пустого списка
    /item/id GET +
        тест 14: корректное получение данных
        тест 15: получение данных несуществующего элемента
        тест 16: получение данных для неавторизованного пользователя
    /item/id PATCH +
        тест 17: корректное обновление элемента
        тест 18: обновление несуществующего элемента
        тест 19: обновление с некорректными полями
        тест 20: обновление от обычного пользователя
    /item/id DELETE
        тест 21: корректное удаление элемента
        тест 22: удаление несуществующего элемента
        тест 23: удаление от обычного пользователя
    /category/id DELETE
        тест 24: корректное удаление категории
        тест 25: удаление несуществующей категории
        тест 26: удаление от обычного пользователя
    """

    def test_add_category(self, db, client, get_admin_headers):
        """ Корректное создание категории """
        response = client.post(
            "/api/inventory/new/category",
            headers=get_admin_headers,
            json=CATEGORY_1
        )

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == CATEGORY_1["name"]

    def test_exists_category(self, db, client, add_category, get_admin_headers):
        """ Добавление уже существующей категории """
        response = client.post(
            "/api/inventory/new/category",
            headers=get_admin_headers,
            json=CATEGORY_1
        )

        assert response.status_code == 409

    def test_add_category_from_user(self, db, client, get_user_headers):
        """ Корректное создание категории """
        response = client.post(
            "/api/inventory/new/category",
            headers=get_user_headers,
            json=CATEGORY_1
        )

        assert response.status_code == 403

    def test_add_item(self, db, client, add_category, get_admin_headers):
        """ Корректное добавление элемента """
        response = client.post(
            "/api/inventory/new/item",
            headers=get_admin_headers,
            json=ITEM_1
        )

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == ITEM_1["name"]
        assert data["category_data"]["id"] == ITEM_1["category_id"]
        assert data["company_id"] == ITEM_1["company_id"]

    def test_add_exists_item(self, db, client, add_item, get_admin_headers):
        """ Добавление уже существующего элемента """
        response = client.post(
            "/api/inventory/new/item",
            headers=get_admin_headers,
            json=ITEM_1
        )

        assert response.status_code == 409

    def test_add_item_from_user(self, db, client, get_user_headers):
        """ Добавление элемента от пользователя """
        response = client.post(
            "/api/inventory/new/item",
            headers=get_user_headers,
            json=ITEM_1
        )

        assert response.status_code == 403

    def test_add_item_with_incorrect_category(self, db, client, get_admin_headers):
        """ Добавление элемента с несуществующей категорией """
        response = client.post(
            "/api/inventory/new/item",
            headers=get_admin_headers,
            json=ITEM_1
        )

        assert response.status_code == 400

    def test_add_item_with_incorrect_quantity(self, db, client, get_admin_headers, add_category):
        """ Добавление элемента с некорректным количеством """
        copy = ITEM_1.copy()
        copy["total_quantity"] = -1
        response = client.post(
            "/api/inventory/new/item",
            headers=get_admin_headers,
            json=copy
        )

        assert response.status_code == 422

    def test_get_list(self, db, client, add_item, get_user_headers):
        """ Корректное получение списка """
        response = client.get(
            "/api/inventory/list?page=1&count_items=10",
            headers=get_user_headers
        )

        assert response.status_code == 200
        data = response.json()

        assert data["page"] == 1
        assert data["count_items"] == 1
        assert len(data["items"]) == 1

    def test_get_list_with_incorrect_page(self, db, client, add_item, get_user_headers):
        """ Получение списка с некорректной страницей """
        response = client.get(
            "/api/inventory/list?page=0&count_items=10",
            headers=get_user_headers
        )

        assert response.status_code == 422

    def test_get_list_with_filters(self, db, client, add_item, get_user_headers):
        """ Получение списка с фильтрами """
        response = client.get(
            f"/api/inventory/list?page=1&count_items=10&category_filters={CATEGORY_1["id"]}",
            headers=get_user_headers
        )

        assert response.status_code == 200
        data = response.json()

        assert data["page"] == 1
        assert data["count_items"] == 1
        assert len(data["items"]) == 1

    def test_get_empty_list(self, db, client, add_item, get_user_headers):
        """ Получение пустого списка """
        response = client.get(
            f"/api/inventory/list?page=1&count_items=10&category_filters={uuid.uuid4()}",
            headers=get_user_headers
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 0

    def test_get_item(self, db, client, add_item, get_user_headers):
        """ Получение данных элемента """
        response = client.get(
            f"/api/inventory/item/{ITEM_1["id"]}",
            headers=get_user_headers
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == ITEM_1["id"]

    def test_get_non_exist_item(self, db, client, get_user_headers):
        """ Получение данных несуществующего элемента """
        response = client.get(
            f"/api/inventory/item/{uuid.uuid4()}",
            headers=get_user_headers
        )

        assert response.status_code == 404

    def test_update_item(self, db, client, add_item, get_admin_headers):
        """ Корректное обновление элемента """
        new_name = "NewName"
        response = client.patch(
            f"/api/inventory/item/{ITEM_1["id"]}",
            headers=get_admin_headers,
            json={"name": new_name}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == new_name
        assert data["id"] == ITEM_1["id"]

    def test_update_non_exist_item(self, db, client, get_admin_headers):
        """ Обновление несуществующего элемента """
        new_name = "NewName"
        response = client.patch(
            f"/api/inventory/item/{uuid.uuid4()}",
            headers=get_admin_headers,
            json={"name": new_name}
        )

        assert response.status_code == 404

    def test_update_item_with_incorrect_fields(self, db, client, add_item, get_admin_headers):
        """ Обновление элемента с несуществующими полями """
        new_name = "NewName"
        response = client.patch(
            f"/api/inventory/item/{ITEM_1["id"]}",
            headers=get_admin_headers,
            json={"test": new_name}
        )

        assert response.status_code == 422

    def test_update_item_from_user(self, db, client, add_item, get_user_headers):
        """ Обновление элемента от обычного пользователя """
        new_name = "NewName"
        response = client.patch(
            f"/api/inventory/item/{ITEM_1["id"]}",
            headers=get_user_headers,
            json={"name": new_name}
        )

        assert response.status_code == 403

    def test_delete_item(self, db, client, add_item, get_admin_headers):
        """ Корректное удаление элемента """
        response = client.delete(
            f"/api/inventory/item/{ITEM_1["id"]}",
            headers=get_admin_headers
        )

        assert response.status_code == 200
        assert InventoryDAO.get_by_id(ITEM_1["id"]) is None

    def test_delete_non_exist_item(self, db, client, get_admin_headers):
        """ Удаление несуществующего элемента """
        response = client.delete(
            f"/api/inventory/item/{uuid.uuid4()}",
            headers=get_admin_headers
        )

        assert response.status_code == 404

    def test_delete_item_from_user(self, db, client, add_item, get_user_headers):
        """ Удаление элемента от имени пользователя """
        response = client.delete(
            f"/api/inventory/item/{ITEM_1["id"]}",
            headers=get_user_headers
        )

        assert response.status_code == 403

    def test_delete_category(self, db, client, add_category, get_admin_headers):
        """ Корректное удаление категории """
        response = client.delete(
            f"/api/inventory/category/{CATEGORY_1["id"]}",
            headers=get_admin_headers
        )

        assert response.status_code == 200
        assert CategoryDAO.get_by_id(CATEGORY_1["id"]) is None

    def test_delete_non_exist_category(self, db, client, get_admin_headers):
        """ Удаление несуществующей категории """
        response = client.delete(
            f"/api/inventory/category/{uuid.uuid4()}",
            headers=get_admin_headers
        )

        assert response.status_code == 404

    def test_delete_category_from_user(self, db, client, get_user_headers):
        """ Удаление категории от имени пользователя """
        response = client.delete(
            f"/api/inventory/category/{CATEGORY_1["id"]}",
            headers=get_user_headers
        )

        assert response.status_code == 403