import uuid
from dataclasses import dataclass


@dataclass
class Category:
    """ Модель для хранения данных о категориях инвентаря """
    id: uuid.uuid4()
    company_id: uuid.uuid4()
    name: str


@dataclass
class Inventory:
    """ Модель для хранения данных об элементах инвентаря """
    id: uuid.uuid4()
    company_id: uuid.uuid4()
    category_id: uuid.uuid4()
    name: str
    total_quantity: int
