from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from src.domain.entities import Post
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
