# Lab: HTTP failure versus transport failure

**ID:** `linux-network` · Python 3.11+ · Outcome: diagnose the failed layer rather than calling every failure “the network.”

Prerequisites: [[60-linux-networking]], [[00-web-foundations]], [[20-python-backend-bridge]]. This uses Python to make local fixtures deterministic; the diagnostic reasoning also applies to curl.

Export `diagnose(url)` from `work/main.py`. Permit only HTTP URLs on `127.0.0.1`, `localhost` or `::1`, with no credentials/fragments and valid ports. Reject other URLs with `ValueError` **before accessing the network**. Do not follow redirects.

An HTTP response returns `{layer:'http',status:NUMBER,ok:BOOLEAN}` where ok means 2xx. A connection failure/timeout returns `{layer:'transport',error:'unreachable'}`. Use a bounded timeout and always close connections.

```bash
python3 90-tools/practice.py start linux-network
python3 90-tools/practice.py check linux-network
```

The checker starts a loopback-only fixture with 200/404/503/302 responses, stops it, then checks connection failure. It never contacts the redirect target or an external site.

Completion: explain why HTTP 503 proves more layers succeeded than connection refusal. Describe a DNS → routing → TCP → TLS → HTTP troubleshooting sequence, including what each tool can and cannot prove. Extend with bounded response-size handling and a separate protocol-error classification.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/linux-network/explanation.md) · [http.client](https://docs.python.org/3/library/http.client.html)
