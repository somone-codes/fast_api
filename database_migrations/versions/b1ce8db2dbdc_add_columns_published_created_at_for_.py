"""add columns published,created_at for posts

Revision ID: b1ce8db2dbdc
Revises: a59c568b90d4
Create Date: 2022-01-07 01:55:14.041020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1ce8db2dbdc'
down_revision = 'a59c568b90d4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False))
    op.add_column("posts",
                  sa.Column(
                    "created_at",
                    sa.TIMESTAMP(timezone=True),
                    server_default=sa.func.now(),
                    nullable=False
                  )
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
