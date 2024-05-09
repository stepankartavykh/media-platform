"""change uniqueness of column

Revision ID: 646f34c55515
Revises: 321168df1c95
Create Date: 2024-03-11 19:32:09.562843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '646f34c55515'
down_revision: Union[str, None] = '321168df1c95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'source', ['url'])


def downgrade() -> None:
    op.drop_constraint(None, 'source', type_='unique')
