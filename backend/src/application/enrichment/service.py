from typing import Optional

from src.infrastructure.persistence.mappers import comment as comment_mapper
from src.infrastructure.scraping import scrape_post_and_comments


def _to_int(v) -> Optional[int]:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _to_float(v) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def enrich_post(uow, browser, post) -> int:
    data = scrape_post_and_comments(browser, post.permalink)
    scraped_post = data.get("post") or {}
    rows = data.get("comments") or []

    post_author = scraped_post.get("author") or post.author
    entities = [
        comment_mapper.feed_to_entity(r, post.id, post_author)
        for r in rows
        if r.get("id")
    ]
    n = uow.comments.upsert_many(entities)

    uow.posts.mark_enriched(
        post.id,
        body=scraped_post.get("body"),
        score=_to_int(scraped_post.get("score")),
        num_comments=_to_int(scraped_post.get("comment_count")),
        upvote_ratio=_to_float(scraped_post.get("upvote_ratio")),
    )
    uow.commit()
    return n
