import argparse
import sys

from src.application.discovery import discover_subreddit
from src.application.enrichment import enrich_post
from src.domain.entities import Subreddit
from src.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.scraping import BrowserSession
from src.settings import settings


def cmd_discover(args) -> int:
    with SQLAlchemyUnitOfWork() as uow:
        uow.subreddits.upsert_many([Subreddit(name=args.subreddit)])
        uow.commit()
        sub = next(s for s in uow.subreddits.list_enabled() if s.name == args.subreddit)
        with BrowserSession(proxy=args.proxy, xvfb=settings.scraper.xvfb) as browser:
            new_ids = discover_subreddit(uow, browser, sub, max_posts=args.max_posts)
    print(f"discovered new posts: {len(new_ids)}")
    return 0


def cmd_enrich(args) -> int:
    with SQLAlchemyUnitOfWork() as uow:
        pending = uow.posts.list_pending(args.limit)
    print(f"pending posts: {len(pending)}")

    with BrowserSession(proxy=args.proxy, xvfb=settings.scraper.xvfb) as browser:
        for post in pending:
            with SQLAlchemyUnitOfWork() as uow:
                fresh = uow.posts.get(post.id)
                try:
                    n = enrich_post(uow, browser, fresh)
                    print(f"  enriched {fresh.reddit_id}: {n} comments")
                except Exception as exc:
                    uow.rollback()
                    uow.posts.mark_failed(fresh.id, str(exc)[:500])
                    uow.commit()
                    print(f"  FAILED {fresh.reddit_id}: {exc}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("discover")
    d.add_argument("--subreddit", required=True)
    d.add_argument("--max-posts", type=int, default=None)
    d.add_argument("--proxy", default=None)
    d.set_defaults(func=cmd_discover)

    e = sub.add_parser("enrich")
    e.add_argument("--limit", type=int, default=5)
    e.add_argument("--proxy", default=None)
    e.set_defaults(func=cmd_enrich)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
