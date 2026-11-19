# Reference: classify observations accurately

The reference parses and restricts the URL before connecting, uses a bounded HTTPConnection, does not follow redirects and closes the connection in finally. A non-2xx response is an HTTP-layer failure, not absence of a connection.

The exercise combines unreachable/timeout observations under one transport label. It does not diagnose every DNS, TLS or malformed-protocol case; its HTTP-only loopback scope is intentional. Verification: `python3 90-tools/practice.py check linux-network --reference`.
