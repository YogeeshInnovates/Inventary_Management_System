"""first  mgration

Revision ID: 4e86333f57af
Revises: bfde5ac40b8a
Create Date: 2025-10-13 12:44:08.550494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e86333f57af'
down_revision: Union[str, Sequence[str], None] = 'bfde5ac40b8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
