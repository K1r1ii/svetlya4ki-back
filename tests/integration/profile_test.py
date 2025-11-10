import uuid

import pytest

from src.auth.auth_dao import UserDAO
from tests.user_utils import USER_2_ID, USER_DATA


@pytest.mark.profile
class TestProfileService:
    """ Тесты эндпоинтов сервиса профиля """

    def test_get_user_by_jwt(self, db, client, register_user, get_user_headers):
        """ Получение пользователя по jwt """
        response = client.get("/api/profile/user", headers=get_user_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(USER_2_ID)

    def test_get_user_by_id(self, db, client, register_user, register_admin, get_admin_headers):
        """ Получение пользователя по id """
        response = client.get("/api/profile/user", params={"id": USER_2_ID}, headers=get_admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(USER_2_ID)

    def test_get_user_for_unauthorized_user(self, db, client, register_user):
        """ Получение пользователя для неавторизованного клиента """
        response = client.get("/api/profile/user", params={"id": USER_2_ID})

        assert response.status_code == 403

    def test_get_user_by_non_exist_id(self, db, client, register_user, get_user_headers):
        """ Получение несуществующего пользователя """
        response = client.get("/api/profile/user", params={"id": uuid.uuid4()}, headers=get_user_headers)

        assert response.status_code == 404

    def test_update_user(self, db, client, register_user, get_user_headers):
        """ Обновление данных пользователя """
        data = {
            "name": "NewName"
        }
        response = client.patch("/api/profile/user", headers=get_user_headers, json=data)

        assert response.status_code == 200
        json = response.json()
        assert json["id"] == str(USER_2_ID)
        assert json["name"] == data["name"]

    def test_update_user_for_unauthorized_user(self, db, client, register_user):
        """ Обновление данных для неавторизованного пользователя """
        data = {
            "name": "NewName"
        }
        response = client.patch("/api/profile/user", json=data)

        assert response.status_code == 403

    def test_update_non_exist_fields(self, db, client, get_user_headers):
        """ Обновление несуществующих полей """
        data = {
            "error_field": "test"
        }
        response = client.patch("/api/profile/user", headers=get_user_headers, json=data)
        assert response.status_code == 422

    def test_update_with_non_unique_data(self, db, client, get_user_headers, register_admin):
        """ Обновление на неуникальные данные """
        data = {
            "email": USER_DATA["email"]
        }
        response = client.patch("/api/profile/user", json=data, headers=get_user_headers)

        assert response.status_code == 400

    def test_delete_user(self, db, client, get_user_headers):
        """ Корректное удаление пользователя """
        response = client.delete("/api/profile/user", headers=get_user_headers)

        assert response.status_code == 200
        assert UserDAO.get_by_id(id=str(USER_2_ID)) is None

    def test_delete_single_admin(self, db, client, get_admin_headers):
        """ Удаление единственного админа """
        response = client.delete("/api/profile/user", headers=get_admin_headers)

        assert response.status_code == 400
        assert UserDAO.get_by_id(USER_DATA["id"]) is not None

    def test_delete_non_single_admin(self, db, client, get_admin_headers, register_user):
        """ Удаление не единственного админа """
        UserDAO.mark_as_admin(str(USER_2_ID))

        response = client.delete("/api/profile/user", headers=get_admin_headers)
        assert response.status_code == 200
        assert UserDAO.get_by_id(str(USER_DATA["id"])) is None

    def test_delete_other_user(self, db, client, get_admin_headers, register_user):
        """ Удаление другого пользователя админом """
        response = client.delete(f"/api/profile/user?id={str(USER_2_ID)}", headers=get_admin_headers)

        assert response.status_code == 200
        assert UserDAO.get_by_id(str(USER_2_ID)) is None

    def test_delete_other_user_without_rights(self, db, client, register_admin, get_user_headers):
        """ Удаление другого пользователя без прав админа """
        response = client.delete(f"/api/profile/user?id={USER_DATA["id"]}", headers=get_user_headers)

        assert response.status_code == 403
        assert UserDAO.get_by_id(USER_DATA["id"]) is not None

    def test_delete_non_exist_user(self, db, client, get_admin_headers):
        """ Удаление не существующего пользователя """
        response = client.delete(f"/api/profile/user?id={str(USER_2_ID)}", headers=get_admin_headers)

        assert response.status_code == 404

    def test_delete_non_authorized_user(self, db, client, register_user):
        """ Удаление для не авторизованного пользователя """
        response = client.delete(f"/api/profile/user?id={str(USER_2_ID)}")

        assert response.status_code == 403

    def test_get_users(self, db, client, get_user_headers, register_admin):
        """ Корректное получение списка пользователей """
        response = client.get("/api/profile/list?page=1&count_items=10", headers=get_user_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) == 2

    def test_get_users_with_incorrect_page(self, db, client, get_user_headers, register_admin):
        """ Получение с некорректным номером страницы """
        response = client.get("/api/profile/list?page=0&count_items=10", headers=get_user_headers)

        assert response.status_code == 422

    def test_get_users_for_non_authorized(self, db, client, register_user):
        """ Получение данных для неавторизованного пользователя """
        response = client.get("/api/profile/list?page=1&count_items=10")

        assert response.status_code == 403

    def test_add_admin(self, db, client, get_admin_headers, register_user):
        """ Корректное добавление нового админа """
        response = client.post(f"/api/profile/add_admin?id={str(USER_2_ID)}", headers=get_admin_headers)

        assert response.status_code == 200
        assert UserDAO.get_by_id(str(USER_2_ID))["is_admin"]

    def test_add_admin_from_user(self, db, client, get_user_headers):
        """ Добавление админа от имени пользователя """
        response = client.post(f"/api/profile/add_admin?id={str(USER_2_ID)}", headers=get_user_headers)

        assert response.status_code == 403
        assert not UserDAO.get_by_id(str(USER_2_ID))["is_admin"]

    def test_add_admin_non_exist_user(self, db, client, get_admin_headers):
        """ Добавление несуществующего пользователя """
        response = client.post(f"/api/profile/add_admin?id={str(uuid.uuid4())}", headers=get_admin_headers)

        assert response.status_code == 404

    def test_re_adding_admin(self, db, client, register_user, get_admin_headers):
        """ Повторное добавление админа """
        UserDAO.mark_as_admin(str(USER_2_ID))
        response = client.post(f"/api/profile/add_admin?id={str(USER_2_ID)}", headers=get_admin_headers)

        assert response.status_code == 409
