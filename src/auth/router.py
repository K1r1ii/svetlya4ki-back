import uuid

from fastapi import APIRouter, HTTPException, status, Depends

from src.auth.auth_dao import UserDAO, InvitationDAO
from src.auth.constants import ACCESS_TOKEN_TYPE
from src.auth.models import User, Invitation
from src.auth.security.jwt import Jwt
from src.auth.shemas import AdminRegisterForm, UserPresent, LoginForm, UserRegisterForm, AccessTokenData, TokensData, \
    Email
from src.auth.utils.dependensies import get_current_user_by_access_token, get_current_user_by_refresh_token
from src.auth.utils.jwt_generate import generate_tokens_pair, invite_token_generate
from src.auth.utils.services import RegisterService
from src.core.responses import CONFLICT, BAD_REQUEST, FORBIDDEN, UNAUTHORIZED, UNPROCESSABLE_ENTITY

router = APIRouter(prefix="/auth", tags=["Аутентификация"], responses=UNPROCESSABLE_ENTITY)


@router.post(path="/register/admin", summary="Регистрация администратора компании", response_model=UserPresent,
             responses=CONFLICT)
def admin_register(data: AdminRegisterForm) -> UserPresent:
    """ Регистрация админа """
    check_user: User = UserDAO().get_by_email(data.email)
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )
    admin: UserPresent = RegisterService.user_register(data, is_admin=True)
    return admin


@router.post(path="/register", summary="Регистрация пользователя по приглашению", response_model=UserPresent,
             responses=BAD_REQUEST | CONFLICT)
def user_register(data: UserRegisterForm) -> UserPresent:
    """ Регистрация пользователя по приглашению """
    invite: Invitation = InvitationDAO.get_by_token(data.token)
    if not invite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Токен некорректный!"
        )
    check = UserDAO.check_user(LoginForm(email=data.email, password=data.password))
    if check:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует!"
        )
    user: UserPresent = RegisterService.user_register(data=data, company_id=invite.company_id)
    RegisterService.mark_invite(invite.id)
    return user


@router.post(path="/invite", summary="Генерация приглашения", responses=FORBIDDEN | UNAUTHORIZED)
async def create_invite(email: Email, user: User = Depends(get_current_user_by_access_token)):
    """ Создание приглашения для регистрации пользователя """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не является администратором"
        )
    check_email: User = UserDAO.get_by_email(email.email)
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )

    token = invite_token_generate()
    invitation: Invitation = InvitationDAO.add_one((str(uuid.uuid4()), str(user.company_id), email.email, token))

    await RegisterService.send_invite_email(email.email, token)
    return {"detail": f"Приглашение отправлено на {email}", "token": token}

@router.post(path="/login", summary="Аутентификация пользователя", response_model=TokensData,
             responses=UNAUTHORIZED)
def login(data: LoginForm):
    """ Аутентификация пользователя """
    user: User = UserDAO.check_user(data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не верные почта или пароль"
        )
    return generate_tokens_pair({"id": str(user.id)})


@router.post(path="/refresh", summary="Обновление токена доступа", response_model=AccessTokenData,
             responses=UNAUTHORIZED)
async def refresh_jwt(user: User = Depends(get_current_user_by_refresh_token)):
    """ Получение токена доступа по рефреш токену """
    data_for_token = {"id": str(user.id)}
    access_token = Jwt.create_jwt_token(data_for_token, ACCESS_TOKEN_TYPE)
    return AccessTokenData(access_token=access_token)
