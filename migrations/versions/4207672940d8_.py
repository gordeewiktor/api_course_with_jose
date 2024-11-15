"""empty message

Revision ID: 4207672940d8
Revises: 0b773427327a
Create Date: 2024-11-10 19:41:50.055660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4207672940d8'
down_revision = '0b773427327a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
