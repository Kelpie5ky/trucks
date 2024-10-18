"""truck and chassis tables1234

Revision ID: bef72302e518
Revises: 6717f7038946
Create Date: 2024-10-17 22:34:25.519629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'bef72302e518'
down_revision: Union[str, None] = '6717f7038946'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chassis',
    sa.Column('brand', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('model', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('wheel_base', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('truck',
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('truck_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('chassis_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('margin', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chassis_id'], ['chassis.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('truck')
    op.drop_table('chassis')
    # ### end Alembic commands ###
