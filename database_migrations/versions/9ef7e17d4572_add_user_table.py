"""add user table

Revision ID: 9ef7e17d4572
Revises: 1907b79b35e1
Create Date: 2022-01-06 21:31:53.120932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef7e17d4572'
down_revision = '1907b79b35e1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),  # alternate way to set primary key
        sa.UniqueConstraint("email")  # alternate way to set unique
    )


def downgrade():
    op.drop_table("users")
