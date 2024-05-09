"""edit fields

Revision ID: 7f8a481b7259
Revises: 82b43bfd68f0
Create Date: 2024-03-09 10:20:30.375838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7f8a481b7259'
down_revision: Union[str, None] = '82b43bfd68f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('article', sa.Column('title', sa.String(), nullable=True))
    op.add_column('article', sa.Column('content', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('article', 'content')
    op.drop_column('article', 'title')
