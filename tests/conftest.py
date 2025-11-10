import uuid

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

from src.auth.auth_dao import InvitationDAO
from src.auth.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.auth.models import Invitation
from src.auth.security.jwt import Jwt
from src.auth.security.password import Password
from src.auth.utils.jwt_generate import invite_token_generate
from src.config import settings
from src.database.dao import BaseDAO
from src.database.db_connection import DatabaseService
from src.main import app
from tests.inventory_utils import CATEGORY_1_TUPLE, ITEM_1_TUPLE
from tests.user_utils import (
    COMPANY_DATA_TUPLE,
    USER_DATA_TUPLE,
    USER_2_DATA_TUPLE,
    COMPANY_ID,
    COMPANY_DATA,
    USER_ID,
    USER_2_ID,
    USER_2_DATA
)


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """Перед всеми тестами — применяем миграции к тестовой БД"""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.get_test_db_url)
    command.upgrade(alembic_cfg, "head")
    # yield
    # alembic_cfg.set_main_option("sqlalchemy.url", settings.get_db_url)


@pytest.fixture(scope="function")
def db():
    """Создаёт новое подключение к тестовой БД для каждого теста"""
    db = DatabaseService(settings.get_test_db_url, test_mode=True)
    BaseDAO.use_db(db) # подмена на тестовую БД
    yield db
    db.conn.rollback()


@pytest.fixture(scope="function")
def add_record(db):
    """ Добавление записей в БД """

    db.execute("INSERT INTO companies (id, name) VALUES(%s, %s);", COMPANY_DATA_TUPLE, fetch=False)
    db.execute(
        """INSERT INTO users (id, company_id, name, surname, phone, email, password, is_admin) VALUES(%s, %s, %s, %s, %s, %s, %s, TRUE);""",
        USER_DATA_TUPLE, fetch=False
    )
    db.execute("INSERT INTO users (id, company_id, name, surname, phone, email, password) VALUES(%s, %s, %s, %s, %s, %s, %s);",
        USER_2_DATA_TUPLE, fetch=False
    )


@pytest.fixture(scope="session")
def client():
    """Клиент FastAPI для запросов к эндпоинтам"""
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def register_company(db):
    """ Регистрация компании """
    db.execute("INSERT INTO companies (id, name) VALUES(%s, %s);", (COMPANY_ID, COMPANY_DATA["name"]), fetch=False)


@pytest.fixture(scope="function")
def register_admin(db, register_company):
    """ Регистрация админа """
    user = list(USER_DATA_TUPLE)
    user[6] = Password.get_password_hash(user[6])
    db.execute(
        """INSERT INTO users (id, company_id, name, surname, phone, email, password, is_admin) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, TRUE);""",
        tuple(user),
        fetch=False
    )


@pytest.fixture(scope="function")
def register_user(db, register_company):
    """ Регистрация пользователя """
    user_2 = list(USER_2_DATA_TUPLE)
    user_2[6] = Password.get_password_hash(user_2[6])
    db.execute(
        """INSERT INTO users (id, company_id, name, surname, phone, email, password) 
        VALUES(%s, %s, %s, %s, %s, %s, %s);""",
        tuple(user_2),
        fetch=False
    )


@pytest.fixture(scope="function")
def get_admin_headers(register_admin):
    """ Получение jwt токена для администратора """
    access_token = Jwt.create_jwt_token({"id": str(USER_ID)}, ACCESS_TOKEN_TYPE)
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="function")
def get_user_headers(register_user):
    """ Получение jwt токена для пользователя """
    access_token = Jwt.create_jwt_token({"id": str(USER_2_ID)}, ACCESS_TOKEN_TYPE)
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="function")
def get_user_refresh():
    """ Получение jwt refresh токена """
    refresh_token = Jwt.create_jwt_token({"id": str(USER_2_ID)}, REFRESH_TOKEN_TYPE)
    return {"Authorization": f"Bearer {refresh_token}"}


@pytest.fixture(scope="function")
def get_invite_token(register_company):
    """ Получение токена приглашения """
    token = invite_token_generate()
    invitation: Invitation = InvitationDAO.add_one((str(uuid.uuid4()), str(COMPANY_ID), USER_2_DATA["email"], token))
    return token


@pytest.fixture(scope="function")
def add_category(db, register_company):
    """ Добавление новой категории """
    db.execute(
        "INSERT INTO categories (id, company_id, name) VALUES (%s, %s, %s);",
        CATEGORY_1_TUPLE,
        fetch=False
    )


@pytest.fixture(scope="function")
def add_item(db, add_category):
    """ Добавление нового элемента """
    db.execute(
        """
            INSERT INTO inventory (id, company_id, category_id, name, total_quantity) 
            VALUES(%s, %s, %s, %s, %s);
        """,
        ITEM_1_TUPLE,
        fetch=False
    )
