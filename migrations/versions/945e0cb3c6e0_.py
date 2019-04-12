"""empty message

Revision ID: 945e0cb3c6e0
Revises: ee0d5db48b15
Create Date: 2019-04-11 15:48:23.947522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '945e0cb3c6e0'
down_revision = 'ee0d5db48b15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('goal', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goals')
    # ### end Alembic commands ###
