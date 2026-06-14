from abc import ABC, abstractmethod

from src.domain.entities import Comment


class ICommentRepository(ABC):
    @abstractmethod
    def upsert_many(self, comments: list[Comment]) -> int:
        raise NotImplementedError
