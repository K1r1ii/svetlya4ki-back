import uuid
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class AdminRegisterForm(BaseModel):
    """ Форма для регистрации администратора и компании """
    company_name: str =  Field(max_length=128, description="Название компании")
    name: str = Field(max_length=32, description="Имя администратора")
    surname: str = Field(max_length=32, description="Фамилия администратора")
    phone: str = Field(description="Номер телефона")
    email: EmailStr = Field(description="Почта")
    password: str = Field(min_length=8, max_length=128, description="Пароль")


class UserRegisterForm(BaseModel):
    """ Форма для регистрации пользователя с токеном приглашения """
    token: str = Field(description="Токен приглашения")
    name: str = Field(max_length=32, description="Имя администратора")
    surname: str = Field(max_length=32, description="Фамилия администратора")
    phone: str = Field(description="Номер телефона")
    email: EmailStr = Field(description="Почта")
    password: str = Field(min_length=8, max_length=128, description="Пароль")


class CompanyData(BaseModel):
    """ Данные о компании """
    id: str = Field(description="Идентификатор компании")
    name: str = Field(max_length=128, description="Название компании")


class UserBrief(BaseModel):
    """ Краткая информация о пользователе (для представления в списке) """
    id: uuid.UUID = Field(description="Идентификатор пользователя")
    name: str = Field(max_length=32, description="Имя пользователя")
    surname: str = Field(max_length=32, description="Фамилия пользователя")
    email: EmailStr = Field(description="Почта")
    is_admin: bool = Field(description="Статус администратора")


class UserPresent(UserBrief):
    """ Данные о пользователя для показа """
    company: CompanyData
    phone: str = Field(description="Номер телефона")
    register_at: datetime = Field(description="Дата регистрации")


class LoginForm(BaseModel):
    """ Форма для аутентификации пользователя """
    email: EmailStr = Field(description="Почта")
    password: str = Field(min_length=8, max_length=128, description="Пароль")


class AccessTokenData(BaseModel):
    access_token: str = Field(description="Токен доступа")


class TokensData(AccessTokenData):
    refresh_token: str = Field(description="Токен восстановления")


class Email(BaseModel):
    """ Форма для почты пользователя """
    email: EmailStr = Field(description="Почта пользователя")
