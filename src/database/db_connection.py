from threading import Lock

import psycopg2.extras
from psycopg2.extras import RealDictRow


class DatabaseService:
    """ Сервис для работы с базой данных """
    _instance= None
    _lock = Lock()

    def __new__(cls, dsn: str):
        """ Использование паттерна singleton для создания только одного подключения к БД """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_connection(dsn)
            return cls._instance

    def _init_connection(self, dsn: str):
        """ Подключение к БД """
        self.dsn = dsn
        self.conn = psycopg2.connect(dsn)
        self.conn.autocommit = True


    def _ensure_connection(self):
        """ Восстановление подключения """
        try:
            self.conn.poll()
        except (psycopg2.InterfaceError, psycopg2.OperationalError):
            self.conn = psycopg2.connect(self.dsn)
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
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchone()

