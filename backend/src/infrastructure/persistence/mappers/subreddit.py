from src.domain.entities import Subreddit
from src.infrastructure.persistence.models import Subreddit as SubredditModel


def to_entity(model: SubredditModel) -> Subreddit:
    return Subreddit(
        id=model.id,
        name=model.name,
        enabled=model.enabled,
    )
