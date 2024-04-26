from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa


class Vote(Base):
    __tablename__ = "votes"
    # id: Mapped[int] = mapped_column(
    #     sa.Integer,
    #     primary_key=True,
    # )

    user_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    post_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    )
