"""invitations table

Revision ID: 705a9b224a93
Revises: 1eead5858077
Create Date: 2025-10-17 22:17:06.332573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '705a9b224a93'
down_revision: Union[str, Sequence[str], None] = '1eead5858077'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Добавление таблицы приглашений """
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS invitations (
            id UUID PRIMARY KEY,
            company_id UUID NOT NULL,
            email VARCHAR(64) NOT NULL UNIQUE,
            token VARCHAR(128) NOT NULL UNIQUE,
            is_used BOOL DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            expire_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '3 days',
            FOREIGN KEY (company_id) REFERENCES companies (id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS invitations")
