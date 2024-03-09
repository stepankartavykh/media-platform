"""add topic table

Revision ID: 8d8e72597e93
Revises: 7f8a481b7259
Create Date: 2024-03-09 12:54:31.122551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '8d8e72597e93'
down_revision: Union[str, None] = '7f8a481b7259'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('topic',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('pid', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['pid'], ['topic.id'], ),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('topic')
