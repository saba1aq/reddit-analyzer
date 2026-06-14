from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.persistence.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.infrastructure.persistence.models.post import Post


class Subreddit(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "subreddits"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="subreddit")
