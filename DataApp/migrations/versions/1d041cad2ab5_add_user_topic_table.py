"""add user topic table

Revision ID: 1d041cad2ab5
Revises: cdb90f95ac75
Create Date: 2024-03-09 13:44:37.210487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '1d041cad2ab5'
down_revision: Union[str, None] = 'cdb90f95ac75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_topic',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('topic_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('user_topic')
