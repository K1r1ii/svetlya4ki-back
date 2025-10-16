"""test_revision

Revision ID: d436e8677aec
Revises: 
Create Date: 2025-10-16 17:57:38.512593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd436e8677aec'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Тестовая миграция """
    op.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name VARCHAR(32) NOT NULL,
        PASSWORD VARCHAR(128) NOT NULL
    );""")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS users;")
