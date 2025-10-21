from datetime import timedelta, datetime, timezone
from typing import Dict

from fastapi import HTTPException, status
from jose import JWTError, jwt

from src.auth.constants import REFRESH_TOKEN_TYPE, ACCESS_TOKEN_TYPE, TOKEN_TYPE_FIELD
from src.config import settings

auth_data = settings.auth_data

class Jwt:
    """ Класс для работы с jwt токеном """
    @classmethod
    def create_jwt_token(cls, data: dict, token_type: str) -> str:
        """ Создание токена """
        payload = data.copy()
        exp_by_type = {
            REFRESH_TOKEN_TYPE: timedelta(days=30),
            ACCESS_TOKEN_TYPE: timedelta(minutes=30)
        }

        exp_time = exp_by_type.get(token_type)
        if exp_time is None:
            raise ValueError("Некорректный тип токена")

        expire = datetime.now(timezone.utc) + exp_time
        payload.update(
            {
                TOKEN_TYPE_FIELD: token_type,
                "iss": "Svetlya4ki",
                "exp": expire,
                "iat": datetime.now(timezone.utc),
            }
        )
        encode_jwt = jwt.encode(payload, auth_data["secret_key"], algorithm=auth_data["algorithm"])
        return encode_jwt

    @classmethod
    def decode_jwt_token(cls, token: str) -> Dict:
        """ Декодирование JWT токена """
        try:
            decoded_token = jwt.decode(token, auth_data["secret_key"], algorithms=auth_data["algorithm"])
            return decoded_token
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid!")