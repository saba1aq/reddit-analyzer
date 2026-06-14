import datetime as dt
import json
import time
from typing import Optional

_EXTRACT_JS = r"""
JSON.stringify(Array.from(document.querySelectorAll('shreddit-post')).map(p => {
  const a = p.querySelector('a[slot="full-post-link"]');
  return {
    full_id: p.getAttribute('id') || '',
    post_id: (p.getAttribute('id') || '').replace(/^t3_/, ''),
    permalink: p.getAttribute('permalink') || '',
    url: a ? a.href : 'https://www.reddit.com' + (p.getAttribute('permalink') || ''),
    title: p.getAttribute('post-title') || '',
    author: p.getAttribute('author') || '',
    subreddit: p.getAttribute('subreddit-name') || '',
    published: p.getAttribute('created-timestamp') || '',
    score: p.getAttribute('score'),
    comments: p.getAttribute('comment-count'),
    upvote_ratio: p.getAttribute('upvote-ratio'),
    post_type: p.getAttribute('post-type') || '',
    domain: p.getAttribute('domain') || '',
  };
}))
"""


def _parse_dt(s: str) -> Optional[dt.datetime]:
    if not s:
        return None
    try:
        d = dt.datetime.fromisoformat(s)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def _to_int(v) -> Optional[int]:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def discover_new(browser, subreddit: str, since: dt.datetime,
                 until: Optional[dt.datetime] = None, *,
                 scroll_px: int = 2200, settle: float = 1.8,
                 max_loops: int = 250, stale_limit: int = 5,
                 max_posts: Optional[int] = None) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/new/"
    browser._open(url)
    time.sleep(4)

    acc: dict[str, dict] = {}
    oldest_seen: Optional[dt.datetime] = None
    stale = 0
    stop_reason = "max_loops cap"

    for loop in range(max_loops):
        try:
            raw = browser.sb.cdp.evaluate(_EXTRACT_JS)
            rows = json.loads(raw) if raw else []
        except Exception as exc:
            print(f"  ! extract error loop {loop}: {exc}")
            rows = []

        new = 0
        round_oldest: Optional[dt.datetime] = None
        for r in rows:
            when = _parse_dt(r["published"])
            if when and (round_oldest is None or when < round_oldest):
                round_oldest = when
            fid = r["full_id"]
            if not fid or fid in acc:
                continue
            acc[fid] = r
            new += 1

        if round_oldest and (oldest_seen is None or round_oldest < oldest_seen):
            oldest_seen = round_oldest

        in_window = sum(
            1 for r in acc.values()
            if (w := _parse_dt(r["published"])) and w >= since
            and (until is None or w < until)
        )
        print(f"  loop {loop + 1}: dom={len(rows)} acc={len(acc)} "
              f"in_window={in_window} oldest={oldest_seen.date() if oldest_seen else '?'}")

        if max_posts and in_window >= max_posts:
            stop_reason = f"reached max_posts={max_posts}"
            break
        if oldest_seen is not None and oldest_seen < since:
            stop_reason = f"crossed since={since.date()}"
            break

        if new == 0:
            stale += 1
            if stale >= stale_limit:
                stop_reason = "feed stopped yielding new posts"
                break
            time.sleep(settle * 1.5)
        else:
            stale = 0

        browser.sb.cdp.scroll_down(scroll_px)
        time.sleep(settle)

    out = []
    for r in acc.values():
        when = _parse_dt(r["published"])
        if when is None or when < since:
            continue
        if until is not None and when >= until:
            continue
        r = dict(r)
        r["score"] = _to_int(r.get("score"))
        r["comments"] = _to_int(r.get("comments"))
        out.append(r)
    out.sort(key=lambda r: r["published"], reverse=True)

    print(f"  scroll stop: {stop_reason}; {len(out)} posts in window "
          f"(scanned {len(acc)} total)")
    return out
