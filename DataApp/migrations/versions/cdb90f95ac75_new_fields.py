"""new fields

Revision ID: cdb90f95ac75
Revises: 8d8e72597e93
Create Date: 2024-03-09 13:25:22.420197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'cdb90f95ac75'
down_revision: Union[str, None] = '8d8e72597e93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('topic', sa.Column('rank', sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column('topic', 'rank')
