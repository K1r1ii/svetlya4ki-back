from threading import Lock

import psycopg2.extras
from psycopg2.extras import RealDictRow

from src.core.exceptions import DatabaseInternalError, DatabaseError


class DatabaseService:
    """ Сервис для работы с базой данных """
    _instance= None
    _lock = Lock()
    _test_mode = False


    def __new__(cls, dsn: str, test_mode: bool = False):
        """ Использование паттерна singleton для создания только одного подключения к БД """
        cls._test_mode = test_mode
        with cls._lock:
            if cls._instance is None or test_mode:
                cls._instance = super().__new__(cls)
                cls._instance._init_connection(dsn)
            return cls._instance

    def _init_connection(self, dsn: str):
        """ Подключение к БД """
        self.dsn = dsn
        self.conn = psycopg2.connect(dsn)
        if self._test_mode:
            self.conn.autocommit = False
        else:
            self.conn.autocommit = True


    def _ensure_connection(self):
        """ Восстановление подключения """
        try:
            self.conn.poll()
        except (psycopg2.InterfaceError, psycopg2.OperationalError):
            self.conn = psycopg2.connect(self.dsn)
            if self._test_mode:
                self.conn.autocommit = False
            else:
                self.conn.autocommit = True

    def execute(self, query: str, params=None, fetch=True) -> list[RealDictRow] | None:
        """ Выполнения запроса к БД """
        self._ensure_connection()
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            return None

    def execute_one(self, query: str, params=None):
        """ Выполнение запроса к БД с возвратом одной записи """
        self._ensure_connection()
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            self.conn.rollback()
            raise DatabaseError(f"Ошибка базы данных: {e}")
        except psycopg2.Error as e:
            self.conn.rollback()
            raise DatabaseInternalError(f"Внутренняя ошибка базы данных: {e}")
