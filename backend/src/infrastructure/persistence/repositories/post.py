import datetime as dt
import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from src.domain.entities import Post
from src.domain.enums import PostStatus
from src.domain.interfaces.repositories import IPostRepository
from src.infrastructure.persistence.mappers import post as post_mapper
from src.infrastructure.persistence.models import Post as PostModel


class PostRepository(IPostRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert_many(self, posts: list[Post]) -> list[str]:
        if not posts:
            return []

        reddit_ids = [p.reddit_id for p in posts]
        existing = set(
            self._session.scalars(
                select(PostModel.reddit_id).where(PostModel.reddit_id.in_(reddit_ids))
            )
        )

        values = [post_mapper.to_insert_dict(p) for p in posts]
        stmt = pg_insert(PostModel).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[PostModel.reddit_id],
            set_={
                "score": stmt.excluded.score,
                "num_comments": stmt.excluded.num_comments,
                "upvote_ratio": stmt.excluded.upvote_ratio,
                "title": stmt.excluded.title,
                "flair": stmt.excluded.flair,
            },
        )
        self._session.execute(stmt)

        return [rid for rid in reddit_ids if rid not in existing]

    def get(self, post_id: uuid.UUID) -> Optional[Post]:
        model = self._session.get(PostModel, post_id)
        return post_mapper.to_entity(model) if model else None

    def get_by_reddit_id(self, reddit_id: str) -> Optional[Post]:
        model = self._session.scalar(
            select(PostModel).where(PostModel.reddit_id == reddit_id)
        )
        return post_mapper.to_entity(model) if model else None

    def list_pending(self, limit: int) -> list[Post]:
        models = self._session.scalars(
            select(PostModel)
            .where(PostModel.status == PostStatus.pending)
            .order_by(PostModel.created_utc.desc())
            .limit(limit)
        ).all()
        return [post_mapper.to_entity(m) for m in models]

    def mark_enriched(self, post_id: uuid.UUID, *, body: Optional[str],
                      score: Optional[int], num_comments: Optional[int],
                      upvote_ratio: Optional[float]) -> None:
        values = {
            "status": PostStatus.enriched,
            "enriched_at": dt.datetime.now(dt.timezone.utc),
            "fetch_error": None,
        }
        if body is not None:
            values["body"] = body
        if score is not None:
            values["score"] = score
        if num_comments is not None:
            values["num_comments"] = num_comments
        if upvote_ratio is not None:
            values["upvote_ratio"] = upvote_ratio
        self._session.execute(
            update(PostModel).where(PostModel.id == post_id).values(**values)
        )

    def mark_failed(self, post_id: uuid.UUID, error: str) -> None:
        self._session.execute(
            update(PostModel)
            .where(PostModel.id == post_id)
            .values(status=PostStatus.failed, fetch_error=error)
        )
