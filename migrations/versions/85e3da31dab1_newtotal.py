"""newtotal

Revision ID: 85e3da31dab1
Revises: d8233604cb1b
Create Date: 2021-08-18 00:58:29.476821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85e3da31dab1'
down_revision = 'd8233604cb1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_consolidation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_order_consolidation_total'), ['total'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_consolidation', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_order_consolidation_total'))
        batch_op.drop_column('total')

    # ### end Alembic commands ###
