from typing import Optional

from sqlalchemy.orm import Session, sessionmaker

from src.domain.interfaces.persistence import IUnitOfWork
from src.domain.interfaces.repositories import IPostRepository, ISubredditRepository
from src.infrastructure.persistence.database import SessionFactory
from src.infrastructure.persistence.repositories.post import PostRepository
from src.infrastructure.persistence.repositories.subreddit import SubredditRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: sessionmaker = SessionFactory) -> None:
        self._session_factory = session_factory
        self._session: Optional[Session] = None
        self._subreddits: Optional[ISubredditRepository] = None
        self._posts: Optional[IPostRepository] = None

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        self._session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None:
            self.rollback()
        self._session.close()
        self._session = None
        self._subreddits = None
        self._posts = None

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("UnitOfWork used outside of context")
        return self._session

    @property
    def subreddits(self) -> ISubredditRepository:
        if self._subreddits is None:
            self._subreddits = SubredditRepository(self.session)
        return self._subreddits

    @property
    def posts(self) -> IPostRepository:
        if self._posts is None:
            self._posts = PostRepository(self.session)
        return self._posts

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def flush(self) -> None:
        self.session.flush()
