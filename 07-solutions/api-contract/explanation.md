# Reference: an explicit HTTP boundary

The factory registers a synchronous health/calculation route, strict bounded request fields, a filtered response model and default OpenAPI JSON. No mutable global state, database or server is created on import. CDN-backed docs pages are disabled for the offline test context.

Verification: `python3 90-tools/practice.py check api-contract --reference`. Tests prove the chosen contract, not network/TLS/deployment behavior or a full security review.
