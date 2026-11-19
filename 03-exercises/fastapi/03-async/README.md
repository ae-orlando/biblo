# FastAPI lab: bounded async work and cleanup

**ID:** api-async. Study [[11-python-async]] and [[05-fastapi-async]] only after the synchronous API units.

Export GatewayError and async total_prices(codes,fetcher,limit=2,timeout=0.2) from work/async_tools.py. Fetch prices concurrently with at most limit in flight, require nonnegative integer prices excluding bool, sum them, enforce a total deadline and cancel/await owned remaining tasks on failure. Invalid limits fail; deadline → TimeoutError; expected upstream/invalid-price failures → GatewayError.

Export create_app(fetcher=None,timeout=0.2,limit=2). POST /totals accepts exactly codes: 1..10 strict strings, trimmed/nonblank and at most 40 characters each. Return {count,total_cents}; invalid requests → 422, GatewayError → generic 502, deadline → 504. Default fake prices A=100, B=250, FREE=0; no external request is made.

```bash
python3 90-tools/practice.py start api-async
python3 90-tools/practice.py check api-async
```

Checks use controlled events and inspect cleanup rather than promised speedups. Completion: explain already-started effects/cancellation limits, catch a missing-bound defect and propose a safe bounded retry policy without implementing indiscriminate retries.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/api-async/explanation.md)
