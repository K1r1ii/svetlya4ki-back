"""users table

Revision ID: 1eead5858077
Revises: 652bb415c8b4
Create Date: 2025-10-17 15:59:37.044670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1eead5858077'
down_revision: Union[str, Sequence[str], None] = '652bb415c8b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Добавление таблицы пользователей """
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            company_id UUID NOT NULL,
            name VARCHAR(32) NOT NULL,
            surname VARCHAR(32) NOT NULL,
            phone VARCHAR(32) NOT NULL UNIQUE,
            email VARCHAR(64) NOT NULL UNIQUE,
            password VARCHAR(128) NOT NULL,
            is_admin BOOL DEFAULT FALSE,
            register_at TIMESTAMPTZ DEFAULT NOW(),
            FOREIGN KEY (company_id) REFERENCES companies (id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(""" DROP TABLE IF EXISTS users """)
