import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.enums import PostStatus
from src.infrastructure.persistence.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.infrastructure.persistence.models.comment import Comment
    from src.infrastructure.persistence.models.subreddit import Subreddit


class Post(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "posts"

    reddit_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    full_id: Mapped[str] = mapped_column(String(24), nullable=False)
    subreddit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subreddits.id"), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    flair: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    post_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    permalink: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    is_self: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    author: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    upvote_ratio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    num_comments: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus, native_enum=False, length=20),
        default=PostStatus.pending,
        nullable=False,
        index=True,
    )
    enriched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    fetch_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    subreddit: Mapped["Subreddit"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_posts_subreddit_id_status", "subreddit_id", "status"),
    )
