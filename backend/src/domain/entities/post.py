import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.enums import PostStatus


@dataclass
class Post:
    reddit_id: str
    full_id: str
    title: str
    permalink: str
    created_utc: datetime
    id: Optional[uuid.UUID] = None
    subreddit_id: Optional[uuid.UUID] = None
    body: Optional[str] = None
    flair: Optional[str] = None
    post_type: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    is_self: Optional[bool] = None
    author: Optional[str] = None
    score: Optional[int] = None
    upvote_ratio: Optional[float] = None
    num_comments: Optional[int] = None
    status: PostStatus = PostStatus.pending
    enriched_at: Optional[datetime] = None
    fetch_error: Optional[str] = None
