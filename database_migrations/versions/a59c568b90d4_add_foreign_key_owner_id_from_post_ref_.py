"""add foreign key owner_id from post ref id in user

Revision ID: a59c568b90d4
Revises: 9ef7e17d4572
Create Date: 2022-01-06 21:51:25.696467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a59c568b90d4'
down_revision = '9ef7e17d4572'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_user_fk",
        source_table="posts",
        local_cols=["owner_id"],
        referent_table="users",
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint("posts_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
