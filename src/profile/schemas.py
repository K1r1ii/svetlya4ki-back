from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.auth.shemas import UserBrief


class UserUpdate(BaseModel):
    """ Модель для обновления данных пользователя """
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class Message(BaseModel):
    """ Модель для отправки сообщений пользователям """
    message: str = Field(max_length=256, description="Текст сообщения")


class Pagination(BaseModel):
    """ Данные для реализации пагинации списков """
    page: int = Field(gt=0, description="Номер страницы")
    count_items: int = Field(ge=1, description="Количество элементов на странице")


class UsersList(Pagination):
    """ Модель для представления списка пользователей """
    users: list[UserBrief]
