import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.persistence.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.infrastructure.persistence.models.post import Post


class Comment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "comments"

    reddit_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    post_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parent_reddit_id: Mapped[Optional[str]] = mapped_column(String(24), nullable=True)

    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    depth: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_submitter: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_utc: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    permalink: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    post: Mapped["Post"] = relationship(back_populates="comments")
