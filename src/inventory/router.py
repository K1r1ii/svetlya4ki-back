import uuid

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends, Query

from src.auth.models import User
from src.auth.utils.dependensies import get_current_user_by_access_token
from src.inventory.inventory_dao import InventoryDAO, CategoryDAO
from src.inventory.models import Inventory
from src.inventory.schemas import (
    InventoryItemPresent,
    AddInventoryForm,
    CategoryPresent,
    AddCategoryForm,
    InventoryList, InventoryUpdate
)
from src.inventory.utils.services import InventoryService
from src.profile.schemas import Pagination, Message

router = APIRouter(prefix="/inventory", tags=["Инвентарь"])


@router.post(path="/new/category", summary="Добавление новой категории", response_model=CategoryPresent)
def add_category(data: AddCategoryForm, user: User = Depends(get_current_user_by_access_token)) -> CategoryPresent:
    """ Добавление новой категории """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нужно быть администратором для доступа к этому ресурсу"
        )
    category: CategoryPresent = InventoryService.add_category(data.name, user.company_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректные данные"
        )
    return category


@router.post(path="/new/item", summary="Добавление нового элемента", response_model=InventoryItemPresent)
def add_item(data: AddInventoryForm, user: User = Depends(get_current_user_by_access_token)) -> InventoryItemPresent:
    """ Добавление нового инвентаря (для админа) """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нужно быть администратором для доступа к этому ресурсу"
        )
    inventory: InventoryItemPresent = InventoryService.add_item(data, user.company_id)
    return inventory


@router.get(path="/list", summary="Список элементов инвентаря", response_model=InventoryList)
def get_items(
        user: User = Depends(get_current_user_by_access_token),
        pagination: Pagination = Depends(),
        category_filters: list[str] = Query(default=None)
):
    """ Получение списка элементов с фильтрами по категориям """
    # TODO: Сделать текущее количество элементов (после сервиса events)+
    data = InventoryDAO.get_items(category_filters, pagination)
    return InventoryList(
        items=[InventoryItemPresent(category_data=CategoryPresent(id=item["category_id"], name=item["category_name"]),**item) for item in data],
        page=pagination.page, count_items=len(data)
    )


@router.get(path="/item/{item_id}", summary="Подробные данные одного элемента", response_model=InventoryItemPresent)
def get_item(item_id: uuid.UUID, user: User = Depends(get_current_user_by_access_token)) -> InventoryItemPresent:
    """ Получение подробной информации об одном элементе """
    item = InventoryDAO.get_by_id(str(item_id))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Элемента с таким id не существует"
        )
    item = Inventory(**item)
    return InventoryService.get_present_view(item)


@router.patch(path="/item/{item_id}", summary="Обновление полей элемента", response_model=InventoryItemPresent)
def update_item(data: InventoryUpdate,
                item_id: uuid.UUID, user: User = Depends(get_current_user_by_access_token)) -> InventoryItemPresent:
    """ Обновление полей одного элемента """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нужно быть администратором для доступа к этому ресурсу"
        )
    check = InventoryDAO.get_by_id(str(item_id))
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Элемента с таким id не существует"
        )
    temp = Inventory(**InventoryDAO.update_one_by_id(data.model_dump(), str(item_id)))
    return InventoryService.get_present_view(temp)


@router.delete(path="/item/{item_id}", summary="Удаление элемента из инвентаря", response_model=Message)
def delete_item(item_id: uuid.UUID, user: User = Depends(get_current_user_by_access_token)) -> Message:
    """ Удаление элемента из инвентаря """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нужно быть администратором для доступа к этому ресурсу"
        )
    check = InventoryDAO.get_by_id(str(item_id))
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Элемента с таким id не существует"
        )
    InventoryDAO.delete_by_id(str(item_id))
    return Message(message="Элемент успешно удален")

@router.delete(path="/category/{category_id}", summary="Удаление категории", response_model=Message)
def delete_category(category_id: uuid.UUID, user: User = Depends(get_current_user_by_access_token)) -> Message:
    """ Удаление категории """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нужно быть администратором для доступа к этому ресурсу"
        )
    check = CategoryDAO.get_by_id(str(category_id))
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категории с таким id не существует"
        )
    CategoryDAO.delete_by_id(str(category_id))
    return Message(message="Категория успешно удалена")