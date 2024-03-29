"""xoa total

Revision ID: 947920a65681
Revises: a1c362ba7c96
Create Date: 2021-08-18 00:54:52.776329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '947920a65681'
down_revision = 'a1c362ba7c96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('daily_order', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'order_consolidation', ['consolidation'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('daily_order', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
