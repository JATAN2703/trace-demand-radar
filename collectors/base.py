"""Shared HTTP plumbing for collectors.

Every collector is expected to fail softly. A radar that dies because one
source went down is worse than one that reports on what it could reach and
says plainly what it could not.
"""

import time
import requests

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")


class Fetcher:
    def __init__(self, delay: float = 0.7, timeout: int = 25, retries: int = 3):
        self.delay = delay
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": UA, "Accept": "application/json"})
        self.errors: list[str] = []

    def get(self, url: str, referer: str | None = None, as_json: bool = True):
        """GET with backoff. Returns None on failure and records the reason."""
        headers = {"Referer": referer} if referer else {}
        for attempt in range(self.retries):
            try:
                time.sleep(self.delay)
                r = self.session.get(url, headers=headers, timeout=self.timeout)
                if r.status_code == 200:
                    return r.json() if as_json else r.text
                # 401/403/429 are decisions by the source, not transient faults.
                # Do not hammer them and do not try to work around them.
                if r.status_code in (401, 403, 429):
                    self.errors.append(f"{url} -> HTTP {r.status_code} (access denied by source)")
                    return None
                if attempt == self.retries - 1:
                    self.errors.append(f"{url} -> HTTP {r.status_code}")
            except Exception as e:
                if attempt == self.retries - 1:
                    self.errors.append(f"{url} -> {type(e).__name__}: {str(e)[:80]}")
            time.sleep(self.delay * (2 ** attempt))
        return None
