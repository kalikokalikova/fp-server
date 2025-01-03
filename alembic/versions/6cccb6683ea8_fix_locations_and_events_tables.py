"""Fix locations and events tables

Revision ID: 6cccb6683ea8
Revises: becc62359526
Create Date: 2024-11-19 17:13:03.590514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cccb6683ea8'
down_revision: Union[str, None] = 'becc62359526'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('location_id', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('events', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(None, 'events', 'locations', ['location_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'updated_at')
    op.drop_column('events', 'created_at')
    op.drop_column('events', 'location_id')
    # ### end Alembic commands ###
