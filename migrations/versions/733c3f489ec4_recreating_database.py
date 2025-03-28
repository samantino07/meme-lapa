"""Recreating database

Revision ID: 733c3f489ec4
Revises: 
Create Date: 2025-03-20 12:46:01.836822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '733c3f489ec4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filename')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meme')
    # ### end Alembic commands ###
