"""empty message

Revision ID: 71cfdeff9084
Revises: c52da2392892
Create Date: 2018-04-17 12:27:27.229218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71cfdeff9084'
down_revision = 'c52da2392892'
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
    sa.Column('size', sa.String(length=40), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('store')
    # ### end Alembic commands ###
