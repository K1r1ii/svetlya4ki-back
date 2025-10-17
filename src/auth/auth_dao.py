from src.auth.models import User, Company
from src.database.dao import BaseDAO


class UserDAO(BaseDAO):
    """ Доступ к таблице пользователей из базы данных """
    __table_name__="users"

    @classmethod
    def get_by_email(cls, email: str) -> User | None:
        """ Поиск пользователя по почте """
        data = cls.db.execute_one("SELECT * FROM users WHERE email = %s", (email,))
        if not data:
            return None
        return User(**data)

    @classmethod
    def add_one(cls, data: tuple):
        """ Добавление нового пользователя """
        user: User = User(**cls.db.execute_one(
            """
                INSERT INTO users (id, company_id, name, surname, phone, email, password, is_admin) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
            """,
            data
        ))
        return user


class CompanyDAO(BaseDAO):
    """ Доступ к таблице компании из базы данных """
    __table_name__="companies"

    @classmethod
    def add_one(cls, data: tuple) -> Company:
        """ Добавление новой компании """
        return Company(**cls.db.execute_one("INSERT INTO companies (id, name) VALUES (%s, %s) RETURNING *", data))
