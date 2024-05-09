"""add table for sources

Revision ID: 321168df1c95
Revises: 080dbc27343b
Create Date: 2024-03-11 09:14:24.528897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '321168df1c95'
down_revision: Union[str, None] = '080dbc27343b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('source',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('url', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('source')
