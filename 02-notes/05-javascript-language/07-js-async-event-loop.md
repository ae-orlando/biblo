---
created: 2026-10-08
updated: 2026-10-21
---

# 07 — Async & Event Loop (promises, `async/await`)

> Prerequisites: functions/closures and arrays. Practice: `js-async`, then `js-http`, in [[practice-catalog]]. Distinguish a mechanism explanation, a deterministic ordering assertion and a performance observation.

## Outcomes

After this note you can: predict run order (normal code, then promise callbacks, then timers); run slow tasks at the same time with `Promise.all` and handle failures; auto-cancel a slow `fetch` after a timeout; avoid the two UI traps: `forEach` with `async` (never waits) and old search results overwriting new ones.

## Mental model
What async means: some work takes time (network, file, timer). Instead of freezing the page, JS starts the work, keeps running other code, and runs a callback when the slow work finishes.
On one JavaScript agent, synchronous work runs to completion. Promise reactions/queueMicrotask run at host-defined microtask checkpoints; the queue is drained before the host continues to later tasks. Browsers have task sources and rendering opportunities; Node has event-loop phases and an additional nextTick queue. “All I/O always after all timers” is not a universal rule. Predict the small example below, but do not extrapolate it into a complete host scheduler model.
What `async` / `await` do: `async function` always returns a promise (a placeholder for a future value). `await` pauses only that function until the promise settles, then gives you the value. Other code keeps running meanwhile.

```js
console.log('1 sync');
queueMicrotask(() => console.log('2 micro'));
setTimeout(() => console.log('3 timer'), 0);
Promise.resolve().then(() => console.log('4 micro'));
console.log('5 sync');
// 1 5 2 4 3 — sync, then micros in order, then timer
```

## Promises (three states, one settlement)
What a promise is: a placeholder object for a value that isn't ready yet. It starts pending, then becomes either fulfilled (has a value) or rejected (has an error). `.then()` runs on success, `.catch()` runs on failure, `.finally()` runs either way. Helpers: `Promise.all` waits for every promise (fails if any fails), `allSettled` waits and reports each result, `race` takes the first to finish, `any` takes the first success.

```js
const ok = Promise.resolve(42);
const bad = Promise.reject(new Error('x'));
bad.catch((e) => console.log('caught:', e.message)); // always handle!
console.log(await ok); // 42 — top-level await works in .mjs + console
const all = await Promise.all([Promise.resolve(1), Promise.resolve(2)]);
console.log(all); // [1,2] — all must succeed
console.log(await Promise.allSettled([ok, bad])); // never rejects — per-result status
console.log(await Promise.race([new Promise((r) => setTimeout(() => r('slow'), 50)), Promise.resolve('fast')]));
// fast — first to settle wins
try { await Promise.any([bad, ok]); console.log('any ok'); } catch { console.log('all failed'); }
// any: first success wins; rejects only if ALL fail (AggregateError)
await ok.finally(() => console.log('cleanup')); // finally: runs either way, passes value through
// ES2024: const { promise, resolve, reject } = Promise.withResolvers(); — external resolve without executor nesting
```

## `async/await` (write async like sync)
What it does: lets you write waiting code top-to-bottom instead of nested callbacks. `throw` inside `async` means rejection (same as returning a rejected promise). `return value` means success. To run two slow tasks at the same time, start both promises first, then `await Promise.all([a, b])`. Awaiting one after the other is slower (serial).

```js
async function get(n) {
  if (n < 0) throw new Error('neg'); // throw === reject
  return n * 2; // return === resolve
}
try {
  console.log(await get(21)); // 42
  await get(-1);
} catch (e) { console.log('err:', e.message); } // err: neg
// Parallel, not serial:
async function both() {
  const [a, b] = await Promise.all([get(1), get(2)]); // concurrent
  return a + b;
}
// Serial (slower, sometimes required):
// const a = await get(1); const b = await get(2);
```

## Timeouts the modern way + UI race guard
Fetch does not expose an application deadline by default. Host/network timeouts may exist, but are not your product's waiting policy. AbortSignal.timeout supplies an explicit abort signal in supported runtimes. A request-number guard suppresses stale results; cancellation and suppression solve related but different problems. Apply the guard to errors as well as successes.

```js
// Explicit application deadline in runtimes supporting AbortSignal.timeout:
// const r = await fetch(url, { signal: AbortSignal.timeout(8000) });
// Manual version (see 09 for full getJSON):
await new Promise((r) => setTimeout(r, 100)); // sleep idiom

// Stale-fetch guard (search-as-you-type must have this):
let latest = 0;
async function search(q) {
  const mine = ++latest;
  const res = await get(q);
  if (mine !== latest) return; // a newer query started — drop this result
  render(res);
}
```

Debounce search inputs (don't fetch per keystroke): wait ~200ms of quiet before `search()`. Throttle scroll/resize handlers similarly.

## `fetch` sketch (full in Fetch note) + timers + Node fs
What the idiom does: `await new Promise(r => setTimeout(r, ms))` sleeps the current async function for `ms` milliseconds. Use it for delays, retries, and demos.

```js
// const r = await fetch('https://api.github.com/zen'); console.log(await r.text());
// Choose an application deadline using AbortController/AbortSignal.timeout (see 09).
await new Promise((r) => setTimeout(r, 100)); // sleep idiom
```

## Pitfalls
- A promise chain with no `catch` (or no `try/catch` around `await`) crashes Node v15+ on rejection — always end chains with handling.
- `arr.forEach(async ...)` starts async work but never waits (returns `undefined`) — use `for...of` with `await`, or `await Promise.all(arr.map(...))`.
- `await` inside a loop runs slow tasks one after another — start independent promises first, then `await Promise.all`.
- Top-level await works in ESM, including .mjs and .js configured as modules; not ordinary CommonJS. REPL/console support is host-specific.
- `setTimeout(..., 0)` still runs after all promise callbacks — never rely on timer timing for order.
- Promise.race does not cancel losing operations. Clear timers you created and abort underlying operations when supported; racing a promise alone does not release every resource.
- Search UI without loading/error/empty states and without a stale-guard can silently show the wrong (old) result.

## Try it
```bash
node -e 'console.log("1"); setTimeout(()=>console.log("2"),0); Promise.resolve().then(()=>console.log("3")); console.log("4")'
node -e 'const g=async(n)=>{if(n<0)throw new Error("neg"); return n*2}; g(21).then(console.log).catch(console.error)'
node --input-type=module -e 'console.log(await Promise.all([Promise.resolve(1),Promise.resolve(2)]))'
node --input-type=module -e 'console.log(await Promise.any([Promise.reject(1),Promise.resolve(2)]))'
```

## Optional scratch drills (inside js-async/work)
1. `order.mjs`: reproduce `sync→micro→timer` demo with `queueMicrotask` added, then `await`-sleep version proving `await` pauses only its fn. Comment the queue order.
2. `all.mjs`: two fake `delay(v,ms)` promises; show serial (`await` loop, time it) vs `Promise.all` (time it with `Date.now()`). Handle one rejection with `allSettled`, show first-success with `any`, cleanup with `finally`.
3. `ship.mjs` — **race + guard demo**: `search(q)` with artificial delays + stale-guard (`latest` counter) + `AbortSignal.timeout` on the slow path. Prove rapid `search('a'); search('ab')` renders only `ab`.

## Break it
`foreach-trap.mjs`: prove `arr.forEach(async ...)` finishes after `console.log('done')`, then fix with `for...of` + `await` and with `Promise.all(map)`. Log `foreach-async → returns undefined → for-of-or-all(map)` in [[90-js-protips]].

## Check
1. Order: sync, `queueMicrotask`, `then`, `setTimeout(0)` — why?
2. `all` vs `allSettled` vs `any` vs `race` — when each?
3. Why does search-as-you-type need a stale-guard or abort?
Gate: pass `js-async`, prove in-flight limits and result ordering using controlled promises, and explain stale error suppression. Timing serial versus concurrent demos is illustrative measurement, not a nonflaky correctness gate. Independent tasks may benefit from concurrency; dependent tasks require sequencing and large workloads need bounds.

## Related

- [[09-js-fetch-storage|Fetch & Storage]]
- [[11-js-node-http|Node HTTP]]

Sources: [MDN execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model), [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), [Node event loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick). Lab verification: [[implementation-status]].
