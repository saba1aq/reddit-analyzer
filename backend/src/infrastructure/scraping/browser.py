from typing import Optional

from seleniumbase import SB


class BrowserSession:
    def __init__(self, proxy: Optional[str] = None) -> None:
        kwargs = dict(uc=True, test=True, locale_code="en")
        if proxy:
            kwargs["proxy"] = proxy
        self._cm = SB(**kwargs)
        self.sb = None
        self._activated = False

    def __enter__(self) -> "BrowserSession":
        self.sb = self._cm.__enter__()
        self._activated = False
        return self

    def __exit__(self, *exc) -> Optional[bool]:
        return self._cm.__exit__(*exc)

    def _open(self, url: str) -> None:
        if not self._activated:
            self.sb.activate_cdp_mode(url)
            self._activated = True
        else:
            self.sb.cdp.open(url)
