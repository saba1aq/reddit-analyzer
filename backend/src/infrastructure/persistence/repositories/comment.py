from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from src.domain.entities import Comment
from src.domain.interfaces.repositories import ICommentRepository
from src.infrastructure.persistence.mappers import comment as comment_mapper
from src.infrastructure.persistence.models import Comment as CommentModel


class CommentRepository(ICommentRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert_many(self, comments: list[Comment]) -> int:
        if not comments:
            return 0

        deduped = {}
        for c in comments:
            if c.reddit_id:
                deduped[c.reddit_id] = c
        if not deduped:
            return 0

        values = [comment_mapper.to_insert_dict(c) for c in deduped.values()]
        stmt = pg_insert(CommentModel).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[CommentModel.reddit_id],
            set_={
                "score": stmt.excluded.score,
                "body": stmt.excluded.body,
            },
        )
        self._session.execute(stmt)
        return len(values)
