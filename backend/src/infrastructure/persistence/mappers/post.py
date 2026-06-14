import uuid
from datetime import datetime, timezone
from typing import Optional

from src.domain.entities import Post
from src.infrastructure.persistence.models import Post as PostModel


def _to_int(v) -> Optional[int]:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _to_float(v) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _parse_dt(s) -> Optional[datetime]:
    if not s:
        return None
    try:
        d = datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def feed_to_entity(row: dict, subreddit_id: uuid.UUID) -> Post:
    return Post(
        reddit_id=row.get("post_id") or row.get("full_id", "").removeprefix("t3_"),
        full_id=row.get("full_id", ""),
        subreddit_id=subreddit_id,
        title=row.get("title") or "",
        permalink=row.get("permalink") or "",
        url=row.get("url"),
        author=row.get("author"),
        post_type=row.get("post_type"),
        domain=row.get("domain"),
        score=_to_int(row.get("score")),
        num_comments=_to_int(row.get("comments")),
        upvote_ratio=_to_float(row.get("upvote_ratio")),
        created_utc=_parse_dt(row.get("published")),
    )


def to_entity(model: PostModel) -> Post:
    return Post(
        id=model.id,
        reddit_id=model.reddit_id,
        full_id=model.full_id,
        subreddit_id=model.subreddit_id,
        title=model.title,
        body=model.body,
        flair=model.flair,
        post_type=model.post_type,
        domain=model.domain,
        permalink=model.permalink,
        url=model.url,
        is_self=model.is_self,
        author=model.author,
        score=model.score,
        upvote_ratio=model.upvote_ratio,
        num_comments=model.num_comments,
        created_utc=model.created_utc,
        status=model.status,
        enriched_at=model.enriched_at,
        fetch_error=model.fetch_error,
    )


def to_insert_dict(entity: Post) -> dict:
    return {
        "reddit_id": entity.reddit_id,
        "full_id": entity.full_id,
        "subreddit_id": entity.subreddit_id,
        "title": entity.title,
        "body": entity.body,
        "flair": entity.flair,
        "post_type": entity.post_type,
        "domain": entity.domain,
        "permalink": entity.permalink,
        "url": entity.url,
        "is_self": entity.is_self,
        "author": entity.author,
        "score": entity.score,
        "upvote_ratio": entity.upvote_ratio,
        "num_comments": entity.num_comments,
        "created_utc": entity.created_utc,
        "status": entity.status,
    }
