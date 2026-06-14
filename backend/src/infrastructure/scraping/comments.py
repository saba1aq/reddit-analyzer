import json
import time
from typing import Optional

_COMMENTS_JS = r"""
JSON.stringify(Array.from(document.querySelectorAll('shreddit-comment')).map(c => {
  const id = c.getAttribute('thingid') || '';
  const bodyEl = document.getElementById(id + '-post-rtjson-content');
  return {
    id: id,
    parent_id: c.getAttribute('parentid') || c.getAttribute('postid') || '',
    depth: c.getAttribute('depth'),
    author: c.getAttribute('author') || '',
    score: c.getAttribute('score'),
    created: c.getAttribute('created') || '',
    permalink: c.getAttribute('permalink') || '',
    body: bodyEl ? bodyEl.innerText.trim() : '',
  };
}))
"""

_POST_JS = r"""
JSON.stringify((() => {
  const p = document.querySelector('shreddit-post');
  if (!p) return null;
  const id = p.getAttribute('id') || '';
  const bodyEl = document.getElementById(id + '-post-rtjson-content');
  return {
    full_id: id,
    title: p.getAttribute('post-title') || '',
    author: p.getAttribute('author') || '',
    score: p.getAttribute('score'),
    comment_count: p.getAttribute('comment-count'),
    upvote_ratio: p.getAttribute('upvote-ratio'),
    created: p.getAttribute('created-timestamp') || '',
    post_type: p.getAttribute('post-type') || '',
    domain: p.getAttribute('domain') || '',
    permalink: p.getAttribute('permalink') || '',
    body: bodyEl ? bodyEl.innerText.trim() : '',
  };
})())
"""

_CLICK_MORE_JS = r"""
(() => {
  let n = 0;
  for (const fp of document.querySelectorAll('faceplate-partial[src*="/svc/shreddit/more-comments/"]')) {
    const btn = fp.querySelector('button:not([aria-hidden="true"])');
    if (btn) { btn.click(); n++; }
  }
  return n;
})()
"""


def scrape_post_and_comments(browser, permalink: str, *,
                             scroll_px: int = 1400, settle: float = 1.2,
                             max_scrolls: int = 60, stable_limit: int = 6) -> dict:
    url = "https://www.reddit.com" + permalink if permalink.startswith("/") else permalink
    browser._open(url)
    time.sleep(5)

    seen: dict[str, dict] = {}
    stable = 0
    for _ in range(max_scrolls):
        try:
            raw = browser.sb.cdp.evaluate(_COMMENTS_JS)
            rows = json.loads(raw) if raw else []
        except Exception:
            rows = []

        new = 0
        for r in rows:
            cid = r.get("id")
            if cid and cid not in seen:
                seen[cid] = r
                new += 1

        try:
            browser.sb.cdp.evaluate(_CLICK_MORE_JS)
        except Exception:
            pass

        if new == 0:
            stable += 1
            if stable >= stable_limit:
                break
        else:
            stable = 0

        browser.sb.cdp.scroll_down(scroll_px)
        time.sleep(settle)

    post: Optional[dict] = None
    try:
        raw_post = browser.sb.cdp.evaluate(_POST_JS)
        post = json.loads(raw_post) if raw_post else None
    except Exception:
        post = None

    return {"post": post, "comments": list(seen.values())}
