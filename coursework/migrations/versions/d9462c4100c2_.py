"""empty message

Revision ID: d9462c4100c2
Revises: a59d0987683f
Create Date: 2018-04-26 11:30:07.516931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9462c4100c2'
down_revision = 'a59d0987683f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('store',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('image', sa.String(length=40), nullable=True),
    sa.Column('cat', sa.String(length=40), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('sale', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('item_quant', sa.Integer(), nullable=True),
    sa.Column('order_status', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('itemid', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(length=40), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.Column('colour', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['itemid'], ['store.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('concerts', 'date_second')
    op.add_column('post', sa.Column('lktsbnean', sa.String(length=40), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'lktsbnean')
    op.add_column('concerts', sa.Column('date_second', sa.DATETIME(), nullable=True))
    op.drop_table('stock')
    op.drop_table('orders')
    op.drop_table('store')
    # ### end Alembic commands ###