from typing import Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.auth_dao import UserDAO
from src.auth.constants import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.auth.models import User
from src.auth.security.jwt import Jwt

security = HTTPBearer()


def get_token_payload(token_type: str, identity) -> Dict:
    """ Получение данных токена + проверка типа токена """
    token = identity.credentials
    data = Jwt.decode_jwt_token(token)
    type_from_token = data.get(TOKEN_TYPE_FIELD)
    if type_from_token is None or type_from_token != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный тип токена"
        )
    return data


def get_user_by_token(token_data: dict) -> User:
    """ Получение пользователя по данным токена """
    user_id = token_data.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно найти id пользователя в токене доступа"
        )
    data = UserDAO.get_by_id(user_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    user: User = User(**data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    return user


def get_auth_user(token_type: str):
    async def get_user_from_token_type(
            credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        payload = get_token_payload(token_type, credentials)
        user = get_user_by_token(payload)
        return user
    return get_user_from_token_type


get_current_user_by_access_token = get_auth_user(ACCESS_TOKEN_TYPE)
get_current_user_by_refresh_token = get_auth_user(REFRESH_TOKEN_TYPE)
