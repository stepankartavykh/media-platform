"""deletion of article table

Revision ID: e5378b91f395
Revises: a7425a2bec80
Create Date: 2024-03-13 10:42:29.972483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'e5378b91f395'
down_revision: Union[str, None] = 'a7425a2bec80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('article')


def downgrade() -> None:
    op.create_table('article',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='article_user_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='article_pkey'))
