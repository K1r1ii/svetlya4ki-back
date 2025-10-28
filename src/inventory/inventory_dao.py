from src.database.dao import BaseDAO
from src.inventory.models import Inventory, Category
from src.profile.schemas import Pagination


class CategoryDAO(BaseDAO):
    """ Доступ к таблице категорий из базы данных """
    _table_name = "categories"

    @classmethod
    def add_one(cls, data: tuple):
        """ Добавление новой категории """
        category: Category = Category(**cls.db.execute_one(
            """
            INSERT INTO categories (id, company_id, name) VALUES(%s, %s, %s) RETURNING *;
            """,
            data
        ))
        return category

    @classmethod
    def get_by_name(cls, name: str):
        """ Получить категорию по имени """
        return cls.db.execute_one("SELECT * FROM categories WHERE name = %s;", (name,))


class InventoryDAO(BaseDAO):
    """ Доступ к таблице инвентаря из базы данных """
    _table_name = "inventory"

    @classmethod
    def add_one(cls, data: tuple):
        """ Добавление одного элемента """
        item: Inventory = Inventory(**cls.db.execute_one(
            """
            INSERT INTO inventory (id, company_id, category_id, name, total_quantity) 
            VALUES(%s, %s, %s, %s, %s) RETURNING *;
            """,
            data
        ))
        return item

    @classmethod
    def get_items(cls, filters: list["str"], pagination: Pagination) -> dict:
        """ Получение списка элементов с фильтром по категориям """
        limit = pagination.count_items
        offset = (pagination.page - 1) * limit
        return cls.db.execute("""
            SELECT i.*, c.name AS category_name FROM inventory i
            JOIN categories c ON c.id = i.category_id  
            WHERE (ARRAY_LENGTH(%s::uuid[], 1) IS NULL OR c.id = ANY(%s::uuid[]))
            LIMIT %s OFFSET %s;        
        """, (filters, filters, limit, offset))
