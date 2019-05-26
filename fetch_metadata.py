from typing import Optional

from starlette.datastructures import Headers
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class FetchMetadataMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    @staticmethod
    def fetch_metadata_not_sent(fetch_site: Optional[str]) -> bool:
        return fetch_site is None

    @staticmethod
    def same_site_or_browser_initiated(fetch_site: str) -> bool:
        return fetch_site in ("none", "same-site", "same-origin")

    @staticmethod
    def simple_top_level_navigation(fetch_mode: str, method: str) -> bool:
        return fetch_mode == "navigate" and method == "GET"

    def is_allowed(self, scope: dict) -> bool:
        if scope["type"] != "http":
            return True

        headers = Headers(scope=scope)
        fetch_site = headers.get("sec-fetch-site")
        fetch_mode = headers.get("sec-fetch-mode")
        method = scope["method"]

        return (
            self.fetch_metadata_not_sent(fetch_site)
            or self.same_site_or_browser_initiated(fetch_site)
            or self.simple_top_level_navigation(fetch_mode, method)
        )

    @staticmethod
    def default_response(scope: Scope, receive: Receive, send: Send) -> ASGIApp:
        return PlainTextResponse(
            "Disallowed due to invalid fetch metadata", status_code=403
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if self.is_allowed(scope):
            await self.app(scope, receive, send)
        else:
            response = self.default_response(scope, receive, send)
            await response(scope, receive, send)
