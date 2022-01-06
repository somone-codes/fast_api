"""create posts table

Revision ID: 0d01d333af27
Revises: 
Create Date: 2022-01-06 21:11:38.731751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d01d333af27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table("posts")
