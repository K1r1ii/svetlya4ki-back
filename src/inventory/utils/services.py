import uuid

from fastapi import HTTPException, status

from src.inventory.inventory_dao import CategoryDAO, InventoryDAO
from src.inventory.models import Inventory, Category
from src.inventory.schemas import CategoryPresent, AddInventoryForm, InventoryItemPresent


class InventoryService:
    """ Сервис для работы с эндпоинтами инвентаря """
    @classmethod
    def add_category(cls, name: str, company_id: uuid.UUID) -> CategoryPresent:
        """ Добавление новой категории """
        check = CategoryDAO.get_by_name(name)
        if check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такая категория уже существует"
            )
        return CategoryPresent(**CategoryDAO.add_one((str(uuid.uuid4()), company_id, name)).__dict__)

    @classmethod
    def add_item(cls, data: AddInventoryForm, company_id: uuid.UUID) -> InventoryItemPresent:
        """ Добавление нового элемента в инвентарь """
        temp = (
            str(uuid.uuid4()),
            str(company_id),
            str(data.category_id),
            data.name,
            data.total_quantity
        )
        category_data = CategoryDAO.get_by_id(str(data.category_id))
        if not category_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой категории не существует"
            )
        inventory: Inventory = InventoryDAO.add_one(temp)
        return InventoryItemPresent(category_data=CategoryPresent(**category_data), **inventory.__dict__)

    @classmethod
    def get_present_view(cls, inventory: Inventory) -> InventoryItemPresent:
        """ Конвертация в pydantic модель """
        category = CategoryDAO.get_by_id(str(inventory.category_id))
        return InventoryItemPresent(category_data=CategoryPresent(id=category["id"], name=category["name"]),
                                    **inventory.__dict__)