"""initial

Revision ID: b80a546a5a19
Revises: 
Create Date: 2024-10-16 22:33:59.040033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b80a546a5a19'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weather_data',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('temperature', sa.String(length=10), nullable=True),
    sa.Column('wind_speed', sa.String(length=10), nullable=True),
    sa.Column('wind_direction', sa.String(length=10), nullable=True),
    sa.Column('atm_pressure', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('precipitation_amount', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weather_data')
    # ### end Alembic commands ###
