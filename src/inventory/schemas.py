import uuid
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.profile.schemas import Pagination


class AddCategoryForm(BaseModel):
    """ Форма для добавления новой категории """
    name: str = Field(max_length=128, description="Название категории")


class AddInventoryForm(BaseModel):
    """ Форма для добавления нового элемента инвентаря """
    category_id: uuid.UUID = Field(description="id категории")
    name: str = Field(max_length=128, description="Название элемента")
    total_quantity: int = Field(gt=0, description="Общее количество")

class CategoryPresent(AddCategoryForm):
    """ Модель для представления данных категории """
    id: uuid.UUID = Field(description="id категории")


class InventoryItemPresent(BaseModel):
    """  Модель для представления одного элемента инвентаря """
    id: uuid.UUID = Field(description="id элемента")
    category_data: CategoryPresent
    company_id: uuid.UUID = Field(description="id компании")
    name: str = Field(max_length=128, description="Название элемента")
    total_quantity: int = Field(gt=0, description="Общее количество")


class InventoryList(Pagination):
    """ Модель для представления списка инвентаря """
    items: list[InventoryItemPresent] = Field(description="Список инвентаря")


class InventoryUpdate(BaseModel):
    """ Модель для обновления элементов инвентаря """
    name: Optional[str] = None
    total_quantity: Optional[int] = None

    model_config = ConfigDict(extra="forbid")
