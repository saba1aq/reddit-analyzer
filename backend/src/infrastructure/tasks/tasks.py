import random
import time
import uuid

from src.application.discovery import discover_subreddit as discover_subreddit_service
from src.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.tasks.celery_app import app, get_browser
from src.settings import settings


@app.task(
    name="discovery.dispatch"
)
def dispatch_discovery() -> int:
    with SQLAlchemyUnitOfWork() as uow:
        subs = [(str(s.id), s.name) for s in uow.subreddits.list_enabled()]
    for sub_id, name in subs:
        discover_subreddit.delay(sub_id, name)
    return len(subs)


@app.task(
    name="discovery.subreddit",
    bind=True,
    autoretry_for=(Exception,),
    max_retries=2,
    retry_backoff=True,
)
def discover_subreddit(self, sub_id: str, name: str) -> int:
    with SQLAlchemyUnitOfWork() as uow:
        sub = uow.subreddits.get(uuid.UUID(sub_id))
        if sub is None:
            return 0
        new_ids = discover_subreddit_service(
            uow, get_browser(), sub, max_posts=settings.scraper.max_posts
        )

    pause = random.uniform(settings.scraper.pause_min, settings.scraper.pause_max)
    time.sleep(pause)
    return len(new_ids)
