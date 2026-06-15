from typing import Optional

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_process_init, worker_process_shutdown

from src.infrastructure.scraping import BrowserSession
from src.settings import settings

app = Celery(
    "reddit_analyzer",
    broker=settings.broker.url,
    include=["src.infrastructure.tasks.tasks"],
)

app.conf.task_ignore_result = True
app.conf.worker_concurrency = 1
app.conf.worker_prefetch_multiplier = 1
app.conf.broker_heartbeat = 0
app.conf.broker_connection_retry_on_startup = True
app.conf.timezone = "Asia/Almaty"
app.conf.beat_schedule = {
    "daily-discovery": {
        "task": "discovery.dispatch",
        "schedule": crontab(hour=9, minute=0),
    },
}

_browser: Optional[BrowserSession] = None


@worker_process_init.connect
def _init_browser(**kwargs) -> None:
    global _browser
    _browser = BrowserSession(proxy=settings.scraper.proxy, xvfb=settings.scraper.xvfb)
    _browser.__enter__()


@worker_process_shutdown.connect
def _close_browser(**kwargs) -> None:
    global _browser
    if _browser is not None:
        _browser.__exit__(None, None, None)
        _browser = None


def get_browser() -> BrowserSession:
    global _browser
    if _browser is None:
        _browser = BrowserSession(proxy=settings.scraper.proxy, xvfb=settings.scraper.xvfb)
        _browser.__enter__()
    return _browser
