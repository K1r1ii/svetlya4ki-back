from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Password:
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """ Хэширование пароля """
        return pwd_context.hash(password)


    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """ Проверка пароля """
        return pwd_context.verify(plain_password, hashed_password)
