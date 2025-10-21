from src.config import settings
from src.database.db_connection import DatabaseService


class BaseDAO:
    """ Базовый класс для работы с базой данных """
    model=None
    db = DatabaseService(settings.get_db_url)

    @classmethod
    def get_by_id(cls, id: str) -> dict:
        """ Получить запись по id """
        return cls.db.execute_one(f"SELECT * FROM {cls._table_name} WHERE id = %s", (id, ))
