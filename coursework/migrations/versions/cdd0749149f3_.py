"""empty message

Revision ID: cdd0749149f3
Revises: 03b06d0df086
Create Date: 2018-05-14 10:17:58.270197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdd0749149f3'
down_revision = '03b06d0df086'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'cart', 'user', ['userid'], ['id'])
    op.create_foreign_key(None, 'cart', 'stock', ['itemid'], ['id'])
    op.create_foreign_key(None, 'cart', 'stock', ['quantity'], ['stock'])
    op.create_foreign_key(None, 'cart', 'store', ['price'], ['price'])
    # ### end Alembic commands ###
