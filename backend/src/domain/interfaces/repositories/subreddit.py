import uuid
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities import Subreddit


class ISubredditRepository(ABC):
    @abstractmethod
    def list_enabled(self) -> list[Subreddit]:
        raise NotImplementedError

    @abstractmethod
    def get(self, subreddit_id: uuid.UUID) -> Optional[Subreddit]:
        raise NotImplementedError

    @abstractmethod
    def upsert_many(self, subreddits: list[Subreddit]) -> None:
        raise NotImplementedError
