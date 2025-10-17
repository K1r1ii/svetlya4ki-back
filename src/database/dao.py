import uuid

from src.config import settings
from src.database.db_connection import DatabaseService


class BaseDAO:
    model=None
    db = DatabaseService(settings.get_db_url)

    @classmethod
    def get_by_id(cls, id: uuid.uuid4()) -> dict:
        """ Получить запись по id """
        return cls.db.execute_one(f"SELECT * FROM {cls.model.__table_name__} WHERE id = %s", (str(id)))
