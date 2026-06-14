import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from src.domain.entities import Subreddit
from src.domain.interfaces.repositories import ISubredditRepository
from src.infrastructure.persistence.mappers import subreddit as subreddit_mapper
from src.infrastructure.persistence.models import Subreddit as SubredditModel


class SubredditRepository(ISubredditRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_enabled(self) -> list[Subreddit]:
        models = self._session.scalars(
            select(SubredditModel).where(SubredditModel.enabled.is_(True))
        ).all()
        return [subreddit_mapper.to_entity(m) for m in models]

    def get(self, subreddit_id: uuid.UUID) -> Optional[Subreddit]:
        model = self._session.get(SubredditModel, subreddit_id)
        return subreddit_mapper.to_entity(model) if model else None

    def upsert_many(self, subreddits: list[Subreddit]) -> None:
        if not subreddits:
            return
        values = [{"name": s.name, "enabled": s.enabled} for s in subreddits]
        stmt = pg_insert(SubredditModel).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[SubredditModel.name],
            set_={"enabled": stmt.excluded.enabled},
        )
        self._session.execute(stmt)
