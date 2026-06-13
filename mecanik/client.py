"""Official Python client for the Mecanik API.

    from mecanik import MecanikClient

    mecanik = MecanikClient(account_id="YOUR_UUID", token="YOUR_TOKEN")
    result = mecanik.tools.security_headers(url="https://example.com")

Get your account UUID and an API token from https://members.mecanik.dev
(new accounts receive 100 free credits). Docs: https://api.mecanik.dev/docs
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

__all__ = ["MecanikClient", "MecanikError", "Tools"]


class MecanikError(Exception):
    """Raised when an endpoint returns ``success: false`` or a non-2xx status."""

    def __init__(self, message: str, status: int, errors: list[dict]):
        super().__init__(message)
        self.status = status
        self.errors = errors


class MecanikClient:
    def __init__(
        self,
        account_id: str,
        token: str,
        base_url: str = "https://api.mecanik.dev",
        timeout: float = 30.0,
        session: Optional[requests.Session] = None,
    ):
        if not account_id:
            raise ValueError("account_id is required")
        if not token:
            raise ValueError("token is required")
        self.account_id = account_id
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()
        self.tools = Tools(self)

    def raw(self, path: str, body: Optional[Dict[str, Any]] = None, method: str = "POST") -> Dict[str, Any]:
        """Make a request and return the full ``{result, success, errors}`` envelope."""
        url = f"{self.base_url}/v1/client/{self.account_id}{path}"
        headers = {"Authorization": f"Bearer {self.token}"}
        if method.upper() == "POST":
            headers["Content-Type"] = "application/json"
            resp = self._session.post(url, json=body or {}, headers=headers, timeout=self.timeout)
        else:
            resp = self._session.get(url, headers=headers, timeout=self.timeout)
        try:
            return resp.json()
        except ValueError:
            raise MecanikError(f"Invalid JSON response (HTTP {resp.status_code}).", resp.status_code, [])

    def call(self, path: str, body: Optional[Dict[str, Any]] = None, method: str = "POST") -> Any:
        """Call an endpoint and return just the ``result``; raises :class:`MecanikError` on failure."""
        data = self.raw(path, body, method)
        if not data.get("success"):
            errors = data.get("errors") or []
            first = errors[0] if errors else {}
            raise MecanikError(first.get("message", "Request failed."), first.get("code", 0), errors)
        return data.get("result")

    def _tool(self, slug: str, body: Dict[str, Any]) -> Any:
        return self.call(f"/tools/{slug}", body)

    # Account
    def account(self) -> Any:
        return self.call("/account", method="GET")

    def token_info(self) -> Any:
        return self.call("/account/token", method="GET")

    def credits(self) -> Any:
        return self.call("/account/credits", method="GET")

    def list_tools(self) -> Any:
        return self.call("/tools", method="GET")


class Tools:
    def __init__(self, client: MecanikClient):
        self._c = client

    # AI-Powered
    def ai_code_review(self, **body: Any) -> Any: return self._c._tool("ai-code-review", body)
    def ai_content_summarize(self, **body: Any) -> Any: return self._c._tool("ai-content-summarize", body)
    def ai_seo_generate(self, **body: Any) -> Any: return self._c._tool("ai-seo-generate", body)
    def ai_translate(self, **body: Any) -> Any: return self._c._tool("ai-translate", body)
    def ai_chat(self, **body: Any) -> Any: return self._c._tool("ai-chat", body)
    def ai_image_generate(self, **body: Any) -> Any: return self._c._tool("ai-image-generate", body)
    def ai_extract(self, **body: Any) -> Any: return self._c._tool("ai-extract", body)
    def ai_alt_text(self, **body: Any) -> Any: return self._c._tool("ai-alt-text", body)
    def ai_moderation(self, **body: Any) -> Any: return self._c._tool("ai-moderation", body)

    # Security & Website Analysis
    def security_headers(self, **body: Any) -> Any: return self._c._tool("security-headers", body)
    def tls_check(self, **body: Any) -> Any: return self._c._tool("tls-check", body)
    def tech_detect(self, **body: Any) -> Any: return self._c._tool("tech-detect", body)
    def seo_analyze(self, **body: Any) -> Any: return self._c._tool("seo-analyze", body)
    def dns_lookup(self, **body: Any) -> Any: return self._c._tool("dns-lookup", body)
    def openapi_validate(self, **body: Any) -> Any: return self._c._tool("openapi-validate", body)
    def subdomain_finder(self, **body: Any) -> Any: return self._c._tool("subdomain-finder", body)
    def exposed_files(self, **body: Any) -> Any: return self._c._tool("exposed-files", body)

    # Email Tools
    def email_deliverability(self, **body: Any) -> Any: return self._c._tool("email-deliverability", body)
    def email_validator(self, **body: Any) -> Any: return self._c._tool("email-validator", body)
    def email_validator_bulk(self, **body: Any) -> Any: return self._c._tool("email-validator-bulk", body)

    # Premium Reports
    def website_audit(self, **body: Any) -> Any: return self._c._tool("website-audit", body)
    def performance_audit(self, **body: Any) -> Any: return self._c._tool("performance-audit", body)
    def broken_link_checker(self, **body: Any) -> Any: return self._c._tool("broken-link-checker", body)
    def carbon_footprint(self, **body: Any) -> Any: return self._c._tool("carbon-footprint", body)

    # Developer Utilities
    def qr_generate(self, **body: Any) -> Any: return self._c._tool("qr-generate", body)
    def placeholder_image(self, query: str) -> Any: return self._c.call(f"/tools/placeholder-image?{query}", method="GET")
    def hash_generate(self, **body: Any) -> Any: return self._c._tool("hash-generate", body)
    def jwt_decode(self, **body: Any) -> Any: return self._c._tool("jwt-decode", body)
    def password_strength(self, **body: Any) -> Any: return self._c._tool("password-strength", body)
    def cron_explain(self, **body: Any) -> Any: return self._c._tool("cron-explain", body)
    def token_counter(self, **body: Any) -> Any: return self._c._tool("token-counter", body)
    def json_to_code(self, **body: Any) -> Any: return self._c._tool("json-to-code", body)
