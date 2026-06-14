from sqlalchemy.orm import Session

from src.domain.interfaces.persistence import IUnitOfWork


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: Session) -> None:
        self._session = session

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()

    def flush(self) -> None:
        self._session.flush()
