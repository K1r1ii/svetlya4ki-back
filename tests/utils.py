import uuid

from src.auth.shemas import AdminRegisterForm

COMPANY_ID = uuid.uuid4()
USER_ID = uuid.uuid4()
USER_2_ID = uuid.uuid4()

USER_DATA = {
  "id": str(USER_ID),
  "company_id": str(COMPANY_ID),
  "name": "TestName",
  "surname": "TestSurname",
  "phone": "8888888888",
  "email": "test@mail.ru",
  "password": "strong_password_123"
}

USER_2_DATA = {
  "id": str(USER_2_ID),
  "company_id": str(COMPANY_ID),
  "name": "TestName",
  "surname": "TestSurname",
  "phone": "99999999999",
  "email": "test2@mail.ru",
  "password": "strong_password_123"
}


USER_DATA_TUPLE = (
  str(USER_ID),
  str(COMPANY_ID),
  "TestName",
  "TestSurname",
  "8888888888",
  "test@mail.ru",
  "strong_password_123"
)

USER_2_DATA_TUPLE = (
  str(USER_2_ID),
  str(COMPANY_ID),
  "TestName",
  "TestSurname",
  "99999999999",
  "test2@mail.ru",
  "strong_password_123"
)

ADMIN_REGISTER = AdminRegisterForm(
  company_name="TestCompany",
  name="TestAdmin",
  surname="TestAdminSurname",
  phone="00000000000",
  email="test@mail.ru",
  password="strong_password_123"
)

COMPANY_DATA = {
  "id": str(COMPANY_ID),
  "name": "TestCompany"
}

COMPANY_DATA_TUPLE = (
  str(COMPANY_ID),
  "TestCompany"
)