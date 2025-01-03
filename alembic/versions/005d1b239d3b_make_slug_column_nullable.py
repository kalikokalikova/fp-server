"""make slug column nullable

Revision ID: 005d1b239d3b
Revises: cbfc63b8b8a8
Create Date: 2024-09-30 18:21:14.735074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '005d1b239d3b'
down_revision: Union[str, None] = 'cbfc63b8b8a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('events', 'slug',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('events', 'slug',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
