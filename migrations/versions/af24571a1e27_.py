"""empty message

Revision ID: af24571a1e27
Revises: a5cffa318ac2
Create Date: 2023-11-30 11:56:07.644257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af24571a1e27'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite__characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True, foreign_key='user.id'),
    sa.Column('characters_id', sa.Integer(), nullable=True, foreign_key='characters.id'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite__characters')
    # ### end Alembic commands ###
