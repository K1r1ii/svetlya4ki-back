import secrets
from unittest.mock import patch

import pytest

from src.auth.auth_dao import UserDAO
from src.auth.security.jwt import Jwt
from src.auth.shemas import LoginForm
from tests.utils import ADMIN_REGISTER, USER_2_DATA


@pytest.mark.auth
class TestAuthService:
    """ Тесты эндпоинтов сервиса авторизации """
    # TODO: добавить тесты для истекших токенов

    # /api/auth/register/admin
    def test_register_admin(self, db, client):
        """ Регистрация администратора """
        response = client.post("/api/auth/register/admin", json=ADMIN_REGISTER.model_dump())

        assert response.status_code == 200
        data = response.json()

        assert data["email"] == ADMIN_REGISTER.email
        assert data["is_admin"] == True

    def test_register_by_exist_email(self, db, client, add_record):
        """ Регистрация админа с уже зарегистрированной почтой """
        response = client.post("/api/auth/register/admin", json=ADMIN_REGISTER.model_dump())

        assert response.status_code == 409
        assert len(db.execute("SELECT * FROM users WHERE email = %s;", (ADMIN_REGISTER.email,))) == 1

    def test_register_with_incorrect_data(self, db, client):
        """ Регистрация админа с некорректными полями """
        response = client.post("api/auth/register/admin", json={
            "company_name": "TestCompany",
            "name": "TestName",
            "surname": "TestSurname",
            "phone": 88888888888,
            "email": "mail",
            "password": "123456789",
            "extra_field": "something"
        })

        assert response.status_code == 422
        assert UserDAO.check_user(LoginForm(email="mail", password="123456789")) is None

    def test_weak_password(self, db, client):
        """ Регистрация со слабым паролем """
        ADMIN_REGISTER.password = "1"
        response = client.post("/api/auth/register/admin", json=ADMIN_REGISTER.model_dump())

        assert response.status_code == 422

    # /api/auth/invite
    def test_invite(self, db, client, register_admin, get_admin_headers):
        """ Генерация токена приглашения с корректными данными """
        with patch("src.auth.router.RegisterService.send_invite_email") as mock_send:
            response = client.post(
                "/api/auth/invite",
                json={"email": USER_2_DATA["email"]},
                headers=get_admin_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "token" in data
            mock_send.assert_called_once_with(USER_2_DATA["email"], data["token"])

    def test_invite_with_exist_email(self, db, client, register_admin, get_admin_headers, register_user):
        """ Генерация приглашения с существующей почтой """
        response = client.post(
            "/api/auth/invite",
            json={"email": USER_2_DATA["email"]},
            headers=get_admin_headers
        )

        assert response.status_code == 409

    def test_invite_for_unauthorized_user(self, db, client):
        """ Генерация приглашения для неавторизованного пользователя (нет токена) """
        response = client.post(
            "/api/auth/invite",
            json={"email": USER_2_DATA["email"]}
        )

        assert response.status_code == 403

    def test_invite_for_non_admin_user(self, db, client, register_user, get_user_headers):
        """ Генерация приглашения для неавторизованного пользователя (нет токена) """
        response = client.post(
            "/api/auth/invite",
            json={"email": USER_2_DATA["email"]},
            headers=get_user_headers
        )

        assert response.status_code == 403

    # /api/auth/register
    def test_register_user(self, db, client, get_invite_token):
        """ Регистрация пользователя по токену приглашения """
        user_data =  USER_2_DATA.copy()
        user_data.pop("id")
        user_data.pop("company_id")
        user_data.update({"token": get_invite_token})

        response = client.post(
            "api/auth/register",
            json=user_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == USER_2_DATA["email"]
        assert UserDAO.get_by_email(user_data["email"]) is not None

    def test_register_user_with_incorrect_token(self, db, client):
        """ Регистрация пользователя с некорректным токеном приглашения """
        user_data = USER_2_DATA.copy()
        user_data.pop("id")
        user_data.pop("company_id")
        user_data.update({"token": secrets.token_urlsafe()})

        response = client.post(
            "api/auth/register",
            json=user_data
        )

        assert response.status_code == 400
        assert UserDAO.get_by_email(USER_2_DATA["email"]) is None

    # /api/auth/login
    def test_login(self, db, client, register_user):
        """ Аутентификация пользователя """
        response = client.post(
            "api/auth/login",
            json={"email": USER_2_DATA["email"], "password": USER_2_DATA["password"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert Jwt.decode_jwt_token(data["access_token"])["id"] == USER_2_DATA["id"]

    def test_login_with_incorrect_data(self, db, client):
        """ Аутентификация пользователя с некорректными данными """
        response = client.post(
            "api/auth/login",
            json={"email": "non@mail.ru", "password": "12345678"}
        )

        assert response.status_code == 401

    # /api/auth/refresh
    def test_refresh(self, db, client, register_user, get_user_refresh):
        """ Обновление по refresh токену """
        response = client.post(
            "/api/auth/refresh",
            headers=get_user_refresh
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_without_refresh(self, db, client, register_user):
        """ Обновление по refresh токену """
        response = client.post(
            "/api/auth/refresh"
        )

        assert response.status_code == 403

    def test_with_incorrect_refresh(self, db, client, register_user, get_user_headers):
        """ Обновление по refresh токену """
        response = client.post(
            "/api/auth/refresh",
            headers=get_user_headers
        )

        assert response.status_code == 401


