import secrets

from src.auth.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.auth.security.jwt import Jwt
from src.auth.shemas import TokensData


def generate_tokens_pair(data: dict):
    """ Генерация токенов """
    access_token = Jwt.create_jwt_token(data, ACCESS_TOKEN_TYPE)
    refresh_token = Jwt.create_jwt_token(data, REFRESH_TOKEN_TYPE)
    return TokensData(access_token=access_token, refresh_token=refresh_token)


def invite_token_generate():
    """ Генерация токена для приглашения """
    return secrets.token_urlsafe(32)