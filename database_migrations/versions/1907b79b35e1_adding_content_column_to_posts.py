"""adding content column to posts

Revision ID: 1907b79b35e1
Revises: 0d01d333af27
Create Date: 2022-01-06 21:27:35.051495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1907b79b35e1'
down_revision = '0d01d333af27'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String()))


def downgrade():
    op.drop_column("posts", "content")
