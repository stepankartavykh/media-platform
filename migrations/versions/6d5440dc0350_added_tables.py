"""added tables

Revision ID: 6d5440dc0350
Revises: 
Create Date: 2024-03-09 09:13:04.629987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '6d5440dc0350'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('fullname', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))
    op.create_table('article',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email_address', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('article')
    op.drop_table('user')
