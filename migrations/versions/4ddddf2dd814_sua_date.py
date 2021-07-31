"""sua date

Revision ID: 4ddddf2dd814
Revises: 641153fbbbf9
Create Date: 2021-07-31 02:43:33.419939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ddddf2dd814'
down_revision = '641153fbbbf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('daily_order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
        batch_op.drop_index('ix_daily_order_order_time')
        batch_op.create_index(batch_op.f('ix_daily_order_date'), ['date'], unique=False)
        batch_op.drop_column('order_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('daily_order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_time', sa.DATETIME(), nullable=True))
        batch_op.drop_index(batch_op.f('ix_daily_order_date'))
        batch_op.create_index('ix_daily_order_order_time', ['order_time'], unique=False)
        batch_op.drop_column('date')

    # ### end Alembic commands ###
