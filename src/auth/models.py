import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Company:
    id: uuid.uuid4()
    name: str
    created_at: datetime


@dataclass
class User:
    id: uuid.uuid4()
    company_id: uuid.uuid4()
    name: str
    surname: str
    phone: str
    email: str
    password: str
    is_admin: bool
    register_at: datetime


@dataclass
class Invitation:
    id: uuid.uuid4()
    company_id: uuid.uuid4()
    email: str
    token: str
    is_used: bool
    created_at: datetime
    expire_at: datetime

