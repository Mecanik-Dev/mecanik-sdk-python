# mecanik (Python)

Official Python client for the [Mecanik API](https://mecanik.dev/en/api/): AI, security analysis, email, reports and developer utility endpoints. Pay-per-use credits, no subscription.

**New accounts get 100 free credits.** Grab your account UUID and an API token at [members.mecanik.dev](https://members.mecanik.dev). Full reference: [api.mecanik.dev/docs](https://api.mecanik.dev/docs).

## Install

```bash
pip install mecanik
```

## Quick start

```python
from mecanik import MecanikClient

mecanik = MecanikClient(account_id="YOUR_ACCOUNT_UUID", token="YOUR_API_TOKEN")

# Each tool returns just the `result`, and raises MecanikError on failure.
headers = mecanik.tools.security_headers(url="https://example.com")
print(headers["grade"], headers["score"])

tokens = mecanik.tools.token_counter(text="Hello world", models=["gpt-4o", "claude-sonnet-4-6"])
audit = mecanik.tools.website_audit(url="https://example.com")
balance = mecanik.credits()  # {"credits": ...}
```

## Error handling

```python
from mecanik import MecanikError

try:
    mecanik.tools.dns_lookup(domain="example.com")
except MecanikError as err:
    print(err.status, str(err), err.errors)
    # status 402 -> out of credits; 403 -> bad token; 429 -> rate limited
```

## Lower-level access

```python
# Full envelope {"result", "success", "errors"}
res = mecanik.raw("/tools/dns-lookup", {"domain": "example.com"})

# Any endpoint by path
result = mecanik.call("/tools/hash-generate", {"input": "hello", "algorithm": "sha256"})
```

## Available tools

`mecanik.tools.*` provides one method per endpoint:

- **AI:** `ai_code_review`, `ai_content_summarize`, `ai_seo_generate`, `ai_translate`, `ai_chat`, `ai_image_generate`, `ai_extract`, `ai_alt_text`, `ai_moderation`
- **Security:** `security_headers`, `tls_check`, `tech_detect`, `seo_analyze`, `dns_lookup`, `openapi_validate`, `subdomain_finder`, `exposed_files`
- **Email:** `email_deliverability`, `email_validator`, `email_validator_bulk`
- **Reports:** `website_audit`, `performance_audit`, `broken_link_checker`, `carbon_footprint`
- **Utilities:** `qr_generate`, `placeholder_image`, `hash_generate`, `jwt_decode`, `password_strength`, `cron_explain`, `token_counter`, `json_to_code`

Account helpers: `account()`, `token_info()`, `credits()`, `list_tools()`.

The machine-readable spec is at [api.mecanik.dev/openapi.json](https://api.mecanik.dev/openapi.json).

## License

MIT
