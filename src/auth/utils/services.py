import uuid

from src.auth.auth_dao import CompanyDAO, UserDAO
from src.auth.models import Company, User
from src.auth.security.password import Password
from src.auth.shemas import AdminRegisterForm, CompanyData, UserPresent


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
    def admin_register(cls, data: AdminRegisterForm) -> UserPresent | None:
        """  Регистрация администратора """
        company_data = CompanyData(id=uuid.uuid4(), name=data.company_name)
        company: Company = cls.__company_register_(data=company_data)
        if company is None:
            return None

        data_tuple = (
            str(uuid.uuid4()),
            str(company.id),
            data.name,
            data.surname,
            data.phone,
            data.email,
            Password.get_password_hash(data.password),
            True
        )
        admin: User = UserDAO.add_one(data_tuple)
        user = UserPresent(
            id=admin.id,
            company=company_data,
            name=admin.name,
            surname=admin.surname,
            phone=admin.phone,
            email=admin.email,
            is_admin=admin.is_admin,
            register_at=admin.register_at
        )
        return user
