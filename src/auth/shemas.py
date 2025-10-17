import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AdminRegisterForm(BaseModel):
    """ Форма для регистрации администратора и компании """
    company_name: str =  Field(max_length=128, description="Название компании")
    name: str = Field(max_length=32, description="Имя администратора")
    surname: str = Field(max_length=32, description="Фамилия администратора")
    phone: str = Field(description="Номер телефона")
    email: str = Field(description="Почта")
    password: str = Field(min_length=8, max_length=128, description="Пароль")

class CompanyData(BaseModel):
    """ Данные о компании """
    id: uuid.UUID = Field(description="Идентификатор компании")
    name: str = Field(max_length=128, description="Название компании")


class UserPresent(BaseModel):
    """ Данные о пользователя для показа """
    id: uuid.UUID = Field(description="Идентификатор пользователя")
    company: CompanyData
    name: str = Field(max_length=32, description="Имя пользователя")
    surname: str = Field(max_length=32, description="Фамилия пользователя")
    phone: str = Field(description="Номер телефона")
    email: str = Field(description="Почта")
    is_admin: bool = Field(description="Статус администратора")
    register_at: datetime = Field(description="Дата регистрации")
