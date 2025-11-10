"""inventories table

Revision ID: 0d37aab9502f
Revises: af7f480e0c05
Create Date: 2025-10-28 20:30:45.599920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d37aab9502f'
down_revision: Union[str, Sequence[str], None] = 'af7f480e0c05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Добавление таблица с инвентарем """
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id UUID PRIMARY KEY,
            company_id UUID NOT NULL,
            category_id UUID NOT NULL,
            name VARCHAR(128) NOT NULL UNIQUE,
            total_quantity INT NOT NULL,
            FOREIGN KEY (company_id) REFERENCES companies (id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories (id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS inventory;")
