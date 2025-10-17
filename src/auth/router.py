from fastapi import APIRouter, HTTPException, status

from src.auth.auth_dao import UserDAO
from src.auth.models import User
from src.auth.shemas import AdminRegisterForm, UserPresent
from src.auth.utils.services import RegisterService

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(path="/register/admin", summary="Регистрация администратора компании")
def admin_register(data: AdminRegisterForm) -> UserPresent:
    check_user: User = UserDAO().get_by_email(data.email)
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )
    admin: UserPresent = RegisterService.admin_register(data)
    return admin


@router.post(path="/register/invite", summary="Регистрация пользователя по приглашению")
def user_register():
    ...


@router.post(path="/invite", summary="Генерация приглашения")
def create_invite():
    ...


@router.post(path="/login", summary="Аутентификация пользователя")
def login():
    ...
