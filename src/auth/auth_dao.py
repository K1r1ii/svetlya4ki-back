from src.auth.models import User, Company, Invitation
from src.auth.security.password import Password
from src.auth.shemas import LoginForm
from src.database.dao import BaseDAO
from src.profile.schemas import Pagination


class UserDAO(BaseDAO):
    """ Доступ к таблице пользователей из базы данных """
    _table_name="users"

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

    @classmethod
    def check_user(cls, data: LoginForm) -> User | None:
        """ Проверка пользователя по почте и паролю """
        user: User = cls.get_by_email(data.email)
        if user is None or not Password.verify_password(data.password, user.password):
            return None
        return user

    @classmethod
    def get_users_by_company(cls, company_id: str, pagination: Pagination) -> list[dict]:
        """ Получение списка пользователей одной компании с пагинацией"""
        return cls.db.execute("SELECT * FROM users WHERE company_id = %s LIMIT %s OFFSET %s;",
                              (company_id, pagination.count_items, (pagination.page - 1)*pagination.count_items)
                              )

    @classmethod
    def get_admins_by_company(cls, company_id: str) -> list[dict]:
        """ Получение списка администраторов одной компании """
        return cls.db.execute("SELECT * FROM users WHERE company_id = %s AND is_admin = TRUE;", (company_id,))

    @classmethod
    def mark_as_admin(cls, id: str):
        """ Сделать пользователя админом """
        cls.db.execute("UPDATE users SET is_admin = TRUE WHERE id = %s;", (id,), fetch=False)


class CompanyDAO(BaseDAO):
    """ Доступ к таблице компании из базы данных """
    _table_name="companies"

    @classmethod
    def add_one(cls, data: tuple) -> Company:
        """ Добавление новой компании """
        return Company(**cls.db.execute_one("INSERT INTO companies (id, name) VALUES (%s, %s) RETURNING *", data))

    @classmethod
    def get_name(cls, id: str) -> str:
        """ Поиск имени компании по id """
        return cls.db.execute_one("SELECT name FROM companies WHERE id = %s;", (id,)).get("name")


class InvitationDAO(BaseDAO):
    """ Доступ к таблице приглашений из базы данных """
    _table_name="invitations"

    @classmethod
    def get_by_token(cls, token: str) -> Invitation | None:
        """ Получение приглашения по токену """
        data = cls.db.execute_one(
            "SELECT * FROM invitations WHERE token = %s AND is_used = FALSE AND expire_at > NOW();",
            (token,)
        )
        if data is None:
            return None
        return Invitation(**data)

    @classmethod
    def add_one(cls, data: tuple) -> Invitation:
        """ Добавление нового приглашения """
        return Invitation(**cls.db.execute_one(
            "INSERT INTO invitations (id, company_id, email, token) VALUES(%s, %s, %s, %s) RETURNING *", data)
        )

    @classmethod
    def mark_used(cls, id: str):
        """ Пометка использованного приглашения """
        cls.db.execute("UPDATE invitations SET is_used = TRUE WHERE id = %s;", (id,), fetch=False)