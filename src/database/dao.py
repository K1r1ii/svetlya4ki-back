from sqlalchemy import values

from src.config import settings
from src.database.db_connection import DatabaseService


class BaseDAO:
    """ Базовый класс для работы с базой данных """
    model=None
    db = DatabaseService(settings.get_db_url)

    @classmethod
    def use_db(cls, db: DatabaseService):
        """ Смена объекта для работы с БД (для подключения тестовой базы данных) """
        cls.db = db

    @classmethod
    def get_by_id(cls, id: str) -> dict:
        """ Получить запись по id """
        return cls.db.execute_one(f"SELECT * FROM {cls._table_name} WHERE id = %s", (id, ))

    @classmethod
    def update_one_by_id(cls, data: dict, id: str):
        """ Обновление одной записи в бд """
        data = {key: value for key, value in data.items() if value}
        columns = [f"{col} = %s" for col in data.keys()]
        new_values = list(data.values())
        new_values.append(id)
        query = f"UPDATE {cls._table_name} SET {", ".join(columns)} WHERE id = %s RETURNING *;"
        return cls.db.execute_one(query, tuple(new_values))

    @classmethod
    def delete_by_id(cls, id: str):
        """ Удаление записи по id """
        cls.db.execute(f"DELETE FROM {cls._table_name} WHERE id = %s", (id,), fetch=False)
