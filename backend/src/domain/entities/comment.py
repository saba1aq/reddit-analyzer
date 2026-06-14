import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    reddit_id: str
    id: Optional[uuid.UUID] = None
    post_id: Optional[uuid.UUID] = None
    parent_reddit_id: Optional[str] = None
    body: Optional[str] = None
    author: Optional[str] = None
    depth: int = 0
    is_submitter: Optional[bool] = None
    score: Optional[int] = None
    created_utc: Optional[datetime] = None
    permalink: Optional[str] = None
