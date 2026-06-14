from abc import ABC, abstractmethod

from src.domain.entities import Post


class IPostRepository(ABC):
    @abstractmethod
    def upsert_many(self, posts: list[Post]) -> list[str]:
        raise NotImplementedError
