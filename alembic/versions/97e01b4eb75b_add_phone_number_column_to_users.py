"""Add phone_number column to users

Revision ID: 97e01b4eb75b
Revises: 0f8542fa1ff0
Create Date: 2024-04-26 13:20:00.956161

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "97e01b4eb75b"
down_revision: Union[str, None] = "0f8542fa1ff0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
