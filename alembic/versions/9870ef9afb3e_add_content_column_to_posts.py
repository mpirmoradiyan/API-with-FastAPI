"""Add content column to posts

Revision ID: 9870ef9afb3e
Revises: 34e31fabe115
Create Date: 2024-04-26 16:50:53.282045

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9870ef9afb3e"
down_revision: Union[str, None] = "34e31fabe115"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
