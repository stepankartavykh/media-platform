"""change column names

Revision ID: 080dbc27343b
Revises: 1d041cad2ab5
Create Date: 2024-03-10 13:32:43.277894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '080dbc27343b'
down_revision: Union[str, None] = '1d041cad2ab5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('username', sa.String(), nullable=True))
    op.drop_column('user', 'fullname')


def downgrade() -> None:
    op.add_column('user', sa.Column('fullname', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('user', 'username')
