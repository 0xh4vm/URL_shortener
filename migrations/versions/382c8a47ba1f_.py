"""empty message

Revision ID: 382c8a47ba1f
Revises: bed886c65722
Create Date: 2021-05-06 17:29:39.503091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '382c8a47ba1f'
down_revision = 'bed886c65722'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_associate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('long', sa.String(length=128), nullable=False),
    sa.Column('short', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url_associate')
    # ### end Alembic commands ###
