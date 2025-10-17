"""companies table

Revision ID: 652bb415c8b4
Revises: d436e8677aec
Create Date: 2025-10-17 10:05:04.345724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '652bb415c8b4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Добавление таблицы с компаниями """
    op.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id UUID PRIMARY KEY,
        name VARCHAR(128) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS companies")
