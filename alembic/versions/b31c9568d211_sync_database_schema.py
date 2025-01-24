"""Sync database schema

Revision ID: b31c9568d211
Revises: 489c5320424b
Create Date: 2024-12-09 19:22:11.357084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b31c9568d211'
down_revision: Union[str, None] = '489c5320424b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Alter the column and specify the existing column type (e.g., VARCHAR(255))
    op.alter_column('events', 'hostname', new_column_name='hostName', existing_type=sa.String(length=255))

def downgrade() -> None:
    # Alter the column back to the original name with the existing column type
    op.alter_column('events', 'hostName', new_column_name='hostname', existing_type=sa.String(length=255))
