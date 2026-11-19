# Lab: bounded concurrency and latest-result state

**ID:** `js-async` · Node 24 · Outcome: reason about asynchronous completion without flaky stopwatch tests.

Prerequisites: [[03-js-functions-scope]], [[05-js-arrays-iterables]], [[07-js-async-event-loop]], [[12-js-errors-regex]].

## Contracts

Export from `work/main.mjs`:
- `latestOnly(worker)`: returns an async wrapper. The newest call resolves `{applied:true,value}` when successful. Superseded calls resolve `{applied:false}`, even if their worker later rejects. A newest-call failure rejects normally. Separate wrapper instances have independent state.
- `mapLimit(items, limit, worker)`: returns a promise of results in input order. No more than `limit` workers are in flight. Limit must be a positive integer. Empty input returns `[]`. Propagate failures; stop scheduling new work once failure is observed. Already-started operations are not magically cancelled.

```bash
python3 90-tools/practice.py start js-async
python3 90-tools/practice.py check js-async
```

Tests use manually resolved promises and barriers to control completion order. Watch the difference between **starting** work and awaiting its result. No exact timer duration is a correctness requirement.

## Completion and transfer

Draw the sequence for two overlapping searches. Explain why `Promise.all` does not cancel outstanding operations. Extend a wrapper to accept an AbortSignal and distinguish cancellation from stale-result suppression; add a regression test proving independent callers remain independent.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/js-async/explanation.md) · [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
