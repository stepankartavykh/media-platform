"""changing models

Revision ID: a7425a2bec80
Revises: 646f34c55515
Create Date: 2024-03-12 08:31:43.095765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a7425a2bec80'
down_revision: Union[str, None] = '646f34c55515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_source',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('source_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('user_source')
