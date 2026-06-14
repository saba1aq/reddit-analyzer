import datetime as dt
from typing import Optional

from src.domain.entities import Subreddit
from src.infrastructure.persistence.mappers import post as post_mapper
from src.infrastructure.scraping.discovery import discover_new


def yesterday_window() -> tuple[dt.datetime, dt.datetime]:
    now = dt.datetime.now(dt.timezone.utc)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return today - dt.timedelta(days=1), today


def discover_subreddit(uow, browser, subreddit: Subreddit, *,
                       since: Optional[dt.datetime] = None,
                       until: Optional[dt.datetime] = None,
                       max_posts: Optional[int] = None) -> list[str]:
    if since is None or until is None:
        since, until = yesterday_window()

    rows = discover_new(browser, subreddit.name, since, until, max_posts=max_posts)
    posts = [post_mapper.feed_to_entity(r, subreddit.id) for r in rows]
    new_ids = uow.posts.upsert_many(posts)
    uow.commit()
    return new_ids
