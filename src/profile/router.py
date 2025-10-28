import uuid

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.auth.auth_dao import UserDAO, CompanyDAO
from src.auth.models import User, Company
from src.auth.shemas import UserPresent, CompanyData, UserBrief
from src.auth.utils.dependensies import get_current_user_by_access_token
from src.core.responses import UNPROCESSABLE_ENTITY, UNAUTHORIZED
from src.profile.schemas import UserUpdate, Message, Pagination, UsersList

router = APIRouter(prefix="/profile", tags=["Профиль пользователя"], responses=UNPROCESSABLE_ENTITY | UNAUTHORIZED)


@router.post(path="/add_admin", summary="Добавить пользователю роль админа", response_model=Message)
def add_admin_role(id: uuid.UUID, user: User = Depends(get_current_user_by_access_token)) -> Message:
    """ Присвоение пользователю роли администратора """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Этот ресурс доступен только администраторам"
        )
    check = UserDAO.get_by_id(str(id))
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователя с таким id не найден"
        )
    if check["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже является администратором"
        )
    UserDAO.mark_as_admin(str(id))
    return Message(message=f"Пользователь {check["name"]} теперь администратор")


@router.get(path="/user", summary="Получить данные пользователя по id или по jwt", response_model=UserPresent)
def get_user(
        id: uuid.UUID = None,
        user: User = Depends(get_current_user_by_access_token)
) -> UserPresent:
    """ Получение данных о пользователе по id или jwt """
    if id is not None:
        data: dict = UserDAO.get_by_id(str(id))
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь с таким id не найден"
            )
        user: User = User(**data)
    company: Company = Company(**CompanyDAO.get_by_id(str(user.company_id)))
    return UserPresent(company=CompanyData(id=company.id, name=company.name), **user.__dict__)


@router.get(path="/list", summary="Получить пользователей одной компании", response_model=UsersList)
def get_users_by_company(pagination: Pagination = Depends(), user: User = Depends(get_current_user_by_access_token)) -> UsersList:
    """ Получение пользователей одной компании """
    data = UserDAO.get_users_by_company(str(user.company_id), pagination)
    if not data:
        return UsersList(users=[], page=pagination.page, count_items=pagination.count_items)
    return UsersList(users=[UserBrief(**user) for user in data], page=pagination.page, count_items=pagination.count_items)

@router.patch(path="/user", summary="Обновить данные профиля", response_model=UserPresent)
def update_profile(data: UserUpdate, user: User = Depends(get_current_user_by_access_token)) -> UserPresent:
    """ Обновление профиля пользователя """
    data: dict = UserDAO.update_one_by_id(data.model_dump(), str(user.id))
    company_name: str = CompanyDAO.get_name(str(user.company_id))
    return UserPresent(company=CompanyData(id=user.company_id, name=company_name), **data)


@router.delete(path="/user", summary="Удаление данных пользователя", response_model=Message)
def delete_user(user: User = Depends(get_current_user_by_access_token), id: uuid.UUID = None) -> Message:
    """ Удаление данных пользователя """
    if user.is_admin:
        if id:
            if id == user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Для удаления своего аккаунта используйте jwt"
                )
            # удаление от админа пользователя с переданным id
            check = UserDAO.get_by_id(str(id))
            if not check:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь с таким id не найден"
                )
            UserDAO.delete_by_id(str(id))
            return Message(message="Аккаунт пользователя успешно удален")
        else:
            admins = UserDAO.get_admins_by_company(user.company_id)
            admins.remove(user.__dict__)
            if not admins:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Нельзя удалить единственного администратора"
                )
            UserDAO.delete_by_id(user.id)
            return Message(message="Аккаунт успешно удален")


    elif not id:
        UserDAO.delete_by_id(user.id)
        return Message(message="Аккаунт успешно удален")
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав для этого ресурса"
        )
