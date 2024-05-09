"""change constraint in Topic model

Revision ID: 7c4c7826b201
Revises: e5378b91f395
Create Date: 2024-03-14 09:35:29.778744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '7c4c7826b201'
down_revision: Union[str, None] = 'e5378b91f395'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('topic', 'pid',
                    existing_type=sa.INTEGER(),
                    nullable=True)


def downgrade() -> None:
    op.alter_column('topic', 'pid',
                    existing_type=sa.INTEGER(),
                    nullable=False)
