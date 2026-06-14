import uuid
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities import Post


class IPostRepository(ABC):
    @abstractmethod
    def upsert_many(self, posts: list[Post]) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get(self, post_id: uuid.UUID) -> Optional[Post]:
        raise NotImplementedError

    @abstractmethod
    def get_by_reddit_id(self, reddit_id: str) -> Optional[Post]:
        raise NotImplementedError

    @abstractmethod
    def list_pending(self, limit: int) -> list[Post]:
        raise NotImplementedError

    @abstractmethod
    def mark_enriched(self, post_id: uuid.UUID, *, body: Optional[str],
                      score: Optional[int], num_comments: Optional[int],
                      upvote_ratio: Optional[float]) -> None:
        raise NotImplementedError

    @abstractmethod
    def mark_failed(self, post_id: uuid.UUID, error: str) -> None:
        raise NotImplementedError
