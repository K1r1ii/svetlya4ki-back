import pytest
from fastapi import HTTPException

from src.auth.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from src.auth.security.jwt import Jwt
from src.auth.utils.dependensies import get_user_by_token
from tests.utils import USER_DATA


@pytest.mark.jwt_unit
class TestUnitJwt:
    """ Unit тесты модулей для работы с jwt """

    def test_create_access_token(self):
        """ Создания access токена """
        payload = {"id": USER_DATA["id"]}
        token = Jwt.create_jwt_token(payload, ACCESS_TOKEN_TYPE)

        assert token is not None
        data = Jwt.decode_jwt_token(token)
        assert data["id"] == USER_DATA["id"]
        assert data[TOKEN_TYPE_FIELD] == ACCESS_TOKEN_TYPE

    def test_create_refresh_token(self):
        """ Создание refresh токена """
        payload = {"id": USER_DATA["id"]}
        token = Jwt.create_jwt_token(payload, REFRESH_TOKEN_TYPE)

        assert token is not None
        data = Jwt.decode_jwt_token(token)
        assert data["id"] == USER_DATA["id"]
        assert data[TOKEN_TYPE_FIELD] == REFRESH_TOKEN_TYPE

    def test_create_token_with_incorrect_type(self):
        """ Создание токена с некорректным типом """
        with pytest.raises(ValueError):
            payload = {"id": USER_DATA["id"]}
            Jwt.create_jwt_token(payload, "incorrect_type")

    def test_decode_incorrect_token(self):
        """ Декодирование некорректного токена """
        with pytest.raises(HTTPException):
            Jwt.decode_jwt_token("incorrect_token")

    def test_get_user_without_id_field(self):
        """ Получение данных пользователя без id """
        with pytest.raises(HTTPException):
            get_user_by_token({"key": "value"})

    def test_get_non_exist_user_by_token(self):
        """ Получение данных о несуществующем пользователе """
        with pytest.raises(HTTPException) as e:
            get_user_by_token({"id": USER_DATA["id"]})
        assert e.value.status_code == 401
