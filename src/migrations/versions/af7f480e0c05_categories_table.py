"""categories table

Revision ID: af7f480e0c05
Revises: 705a9b224a93
Create Date: 2025-10-28 20:13:15.868242

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'af7f480e0c05'
down_revision: Union[str, Sequence[str], None] = '705a9b224a93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Добавление таблицы с категориями """
    op.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id UUID PRIMARY KEY,
        company_id UUID NOT NULL,
        name VARCHAR(32) NOT NULL UNIQUE,
        FOREIGN KEY (company_id) REFERENCES companies (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS categories")
