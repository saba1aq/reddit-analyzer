import uuid
from datetime import datetime, timezone
from typing import Optional

from src.domain.entities import Comment


def _to_int(v) -> Optional[int]:
    try:
        return int(v)
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


def feed_to_entity(row: dict, post_id: uuid.UUID, post_author: Optional[str]) -> Comment:
    author = row.get("author") or None
    reddit_id = (row.get("id") or "").split("_", 1)[-1]
    return Comment(
        reddit_id=reddit_id,
        post_id=post_id,
        parent_reddit_id=row.get("parent_id") or None,
        body=row.get("body") or None,
        author=author,
        depth=_to_int(row.get("depth")) or 0,
        is_submitter=(author is not None and author == post_author),
        score=_to_int(row.get("score")),
        created_utc=_parse_dt(row.get("created")),
        permalink=row.get("permalink") or None,
    )


def to_insert_dict(entity: Comment) -> dict:
    return {
        "reddit_id": entity.reddit_id,
        "post_id": entity.post_id,
        "parent_reddit_id": entity.parent_reddit_id,
        "body": entity.body,
        "author": entity.author,
        "depth": entity.depth,
        "is_submitter": entity.is_submitter,
        "score": entity.score,
        "created_utc": entity.created_utc,
        "permalink": entity.permalink,
    }
