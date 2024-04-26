"""Add owner_id column to posts

Revision ID: 0f8542fa1ff0
Revises: b9bd290a46fb
Create Date: 2024-04-26 13:11:35.595402

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f8542fa1ff0"
down_revision: Union[str, None] = "b9bd290a46fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "owner_id",
            sa.Integer,
            # sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    op.create_foreign_key(
        "posts_owner_id_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_owner_id_fkey", table_name="posts")
    op.drop_column("posts", "owner_id")
