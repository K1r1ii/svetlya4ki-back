import uuid
from fastapi_mail import MessageType, MessageSchema, FastMail

from src.auth.auth_dao import CompanyDAO, UserDAO, InvitationDAO
from src.auth.models import Company, User
from src.auth.security.password import Password
from src.auth.shemas import AdminRegisterForm, CompanyData, UserPresent, UserRegisterForm
from src.config import settings


class RegisterService:
    """ Сервис для регистрации """

    @classmethod
    def __company_register_(cls, data: CompanyData) -> Company | None:
        """ Регистрация компании """
        data_tuple = (
            str(data.id),
            data.name
        )
        return CompanyDAO.add_one(data_tuple)

    @classmethod
    def user_register(cls, data: AdminRegisterForm | UserRegisterForm, is_admin: bool = False, company_id: str = None) -> UserPresent | None:
        """  Регистрация администратора """
        if is_admin:
            company_data = CompanyData(id=str(uuid.uuid4()), name=data.company_name)
            company: Company = cls.__company_register_(data=company_data)
            if company is None:
                return None
        else:
            company_name = CompanyDAO.get_name(company_id)
            company_data = CompanyData(id=company_id, name=company_name)

        data_tuple = (
            str(uuid.uuid4()),
            str(company_data.id),
            data.name,
            data.surname,
            data.phone,
            data.email,
            Password.get_password_hash(data.password),
            is_admin
        )
        new_user: User = UserDAO.add_one(data_tuple)
        user = UserPresent(
            id=new_user.id,
            company=company_data,
            name=new_user.name,
            surname=new_user.surname,
            phone=new_user.phone,
            email=new_user.email,
            is_admin=new_user.is_admin,
            register_at=new_user.register_at
        )
        return user


    @classmethod
    async def send_invite_email(cls, to_email: str, token: str):
        subject = "Добро пожаловать в Svetlya4kiAPI!"
        body = f"""
        <h3>Привет!</h3>
        <p>Перейди по ссылке, чтобы завершить регистрацию:</p>
        <a href="http://127.0.0.1:8000/api/register?token={token}">
            Завершить регистрацию
        </a>
        """

        message = MessageSchema(
            subject=subject,
            recipients=[to_email],
            body=body,
            subtype=MessageType.html
        )
        conf = settings.get_email_conf
        fm = FastMail(conf)
        await fm.send_message(message)


    @classmethod
    def mark_invite(cls, invite_id: str):
        """ Пометка использованного приглашения """
        InvitationDAO.mark_used(invite_id)
