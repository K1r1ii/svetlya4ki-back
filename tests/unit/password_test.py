import passlib.exc
import pytest

from src.auth.security.password import Password
from tests.user_utils import USER_DATA


@pytest.mark.password_unit
class TestPasswordUnit:
    """ Unit тесты модулей для хэширования пароля """

    def test_hash_password(self):
        """ Хэширование пароля """
        password = USER_DATA["password"]
        hash_password = Password.get_password_hash(password)

        assert Password.verify_password(password, hash_password)

    def test_with_incorrect_password(self):
        """  Верификация с неверным паролем """
        password = USER_DATA["password"]
        hash_password = Password.get_password_hash(password)
        wrong_password = "wrong_password"
        assert not Password.verify_password(wrong_password, hash_password)


    def test_verify_password_with_incorrect_hash(self):
        """ Верификация пароля с некорректным хэшем """
        password = USER_DATA["password"]
        with pytest.raises(passlib.exc.UnknownHashError):
            Password.verify_password(password, "incorrect_hash")
