import uuid

import pytest

from src.core.exceptions import DatabaseInternalError, DatabaseError
from tests.user_utils import COMPANY_DATA, COMPANY_DATA_TUPLE, USER_DATA, USER_2_DATA

@pytest.mark.database
class TestDatabaseService:
    """ Тесты сервиса по работе с базой данных """

    """
    Тесты разделены на блоки в соответствии с CRUD операциями
    """

    # CREATE TESTS
    def test_add_one(self, db):
        """ Добавление одной записи в таблицу companies """
        result = db.execute_one("INSERT INTO companies (id, name) VALUES(%s, %s) RETURNING *;",
                       COMPANY_DATA_TUPLE
                       )
        assert result["name"] == COMPANY_DATA["name"]
        assert result["id"] == COMPANY_DATA["id"]

    def test_add_into_non_exists_table(self, db):
        """ Добавление записи в несуществующую таблицу """
        with pytest.raises(DatabaseInternalError):
            db.execute_one("INSERT INTO non-existent-table (id, name) VALUES(%s, %s) RETURNING *;",
                           (str(uuid.uuid4()), "test_name")
                           )

    def test_add_incorrect_data(self, db):
        """ Добавление записи с некорректными данными """
        with pytest.raises(DatabaseError):
            db.execute_one("INSERT INTO companies (id, name) VALUES(%s, %s) RETURNING *;", ("incorrect_id", "TestName"))

    # READ TESTS
    def test_read_one_record(self, add_record, db):
        """ Получение одной записи """
        result = db.execute_one("SELECT * FROM users WHERE id = %s;", (USER_DATA["id"],))

        assert result is not None
        assert result["id"] == USER_DATA["id"]
        assert result["email"] == USER_DATA["email"]

    def test_read_many_records(self, add_record, db):
        """ Получение нескольких записей """
        result = db.execute("SELECT * FROM users WHERE name = %s;", (USER_DATA["name"],))

        assert len(result) == 2
        assert result[0]["id"] == USER_DATA["id"]
        assert result[1]["id"] == USER_2_DATA["id"]

    def test_read_many_non_exist_record(self, add_record, db):
        """ Получение нескольких несуществующих записей """
        result = db.execute("SELECT * FROM users WHERE name = %s;", ("None",))
        assert result == []

    def test_read_one_non_exist_record(self, add_record, db):
        """ Получение несуществующей записи """
        result = db.execute_one("SELECT * FROM users WHERE name = %s;", ("None",))

        assert result is None

    # UPDATE TESTS
    def test_update_record(self, add_record, db):
        """ Обновление существующей записи """
        new_value = "NewName"
        result = db.execute_one(f"UPDATE users SET name = %s WHERE id = %s RETURNING *;", (new_value, USER_DATA["id"]))

        assert result["id"] == USER_DATA["id"]
        assert result["name"] == new_value

    def test_update_non_exist_record(self, add_record, db):
        """ Обновление несуществующей записи """
        with pytest.raises(DatabaseInternalError):
            db.execute_one("UPDATE users SET name = 'NewName' WHERE id = %s;", (uuid.uuid4(),))

    def test_update_many_records(self, add_record, db):
        """ Обновление нескольких записей """
        new_value = "NewName"
        result = db.execute("UPDATE users SET name = %s WHERE name = %s RETURNING *;", (new_value, USER_DATA["name"]))

        assert len(result) == 2

        assert result[0]["id"] == USER_DATA["id"]
        assert result[1]["id"] == USER_2_DATA["id"]

        assert result[0]["name"] == result[1]["name"] == new_value

    # DELETE TESTS
    def test_delete_record(self, add_record, db):
        """ Удаление существующей записи """
        db.execute("DELETE FROM users WHERE id = %s;", (USER_DATA["id"],), fetch=False)
        result = db.execute_one("SELECT * FROM users WHERE id = %s;", (USER_DATA["id"],))

        assert result is None

    def test_delete_non_exist_record(self, add_record, db):
        """ Удаление несуществующей записи """
        db.execute("DELETE FROM users WHERE id = %s;", (uuid.uuid4(),), fetch=False)
        result = db.execute("SELECT * FROM users;")

        assert len(result) == 2

    def test_delete_cascade(self, add_record, db):
        """ Каскадное удаление записей """
        db.execute("DELETE FROM companies WHERE id = %s;", (COMPANY_DATA["id"],), fetch=False)
        users = db.execute("SELECT * FROM users WHERE company_id = %s;", (COMPANY_DATA["id"],))

        assert users == []
