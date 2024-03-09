"""edit fields

Revision ID: 82b43bfd68f0
Revises: 6d5440dc0350
Create Date: 2024-03-09 09:20:14.607408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '82b43bfd68f0'
down_revision: Union[str, None] = '6d5440dc0350'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('article', 'email_address')
    op.add_column('user', sa.Column('email_address', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('user', 'email_address')
    op.add_column('article', sa.Column('email_address', sa.VARCHAR(), autoincrement=False, nullable=False))
