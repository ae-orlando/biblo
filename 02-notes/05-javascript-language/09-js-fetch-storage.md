---
created: 2026-10-08
updated: 2026-10-21
---

# 09 — Fetch & Storage (JSON, URL, `localStorage`)

> Prerequisites: [[07-js-async-event-loop]], [[00-web-foundations]]. Practice: `js-http` and `js-dom` in [[practice-catalog]]. Prefer the bundled local fixtures to public endpoints for repeatable assessment; the public GitHub examples below are optional network demonstrations.

## Outcomes

After this note you can: write a `getJSON` helper that times out, throws on HTTP error status, and checks the reply is JSON; send JSON with POST and files with `FormData`; explain why the browser blocks cross-site reads and which server header fixes it; save/load safely with versioned keys like `todos.v1`.

Serve over `http://localhost` — `fetch` on `file://` fails (CORS).

## Mental model
What `fetch` does: asks a URL for data and returns a promise of a `Response` object. Important: network success is not the same as HTTP success — a 404 still resolves, so you must check `res.ok` yourself. `res.json()` reads and parses the JSON body (bodies can be read only once). `JSON.stringify(obj)` turns an object into text for sending.
What storage does: `localStorage` saves strings in the browser by origin (site), surviving reloads. Always `JSON.stringify` on save and `JSON.parse` on load, wrapped in `try/catch`.
CORS is a browser-controlled mechanism for certain cross-origin reads. Resolve a legitimate integration using an intentional server policy or a same-origin architecture/proxy you control. There is no safe client-side fetch flag that grants a page arbitrary readable cross-origin access. CORS is not authentication and does not stop nonbrowser clients from making requests.

```js
const r = await fetch('https://api.github.com/zen');
console.log(r.ok, r.status); // true 200 — must check; 404 still resolves!
console.log(await r.text());
```

## A fetch pattern for an explicit application/json contract
What it does: `getJSON` fetches with a timeout (aborts if too slow), throws on HTTP error status, throws if the reply is not JSON, otherwise returns the parsed object. The `finally` clears the timer either way.

```js
async function getJSON(url, { timeout = 8000 } = {}) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), timeout); // or signal: AbortSignal.timeout(timeout)
  try {
    const res = await fetch(url, { signal: ctl.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
    const ct = res.headers.get('content-type') ?? '';
    if (!ct.includes('application/json')) throw new TypeError(`expected JSON, got ${ct}`);
    return await res.json(); // or .text()/.blob()/.formData() for non-JSON
  } finally { clearTimeout(t); }
}
// POST JSON:
// await fetch('/api/todos', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: 'hi' }) });
// Upload files: const fd = new FormData(); fd.append('file', fileInput.files[0]); await fetch('/upload', { method: 'POST', body: fd }); // no Content-Type — browser sets multipart boundary
// Authed: await fetch(url, { headers: { Authorization: `Bearer ${token}` }, credentials: 'include' });
```

## CORS (why your `fetch` is blocked, and the real fix)

- Same-origin page/API requests avoid the CORS cross-origin requirement, but can still fail through network, HTTP, authentication, content/security policy or application errors. The capstone explicitly defines serving both assets and API.
- Cross-origin: page `:8000` → API `:3000` needs server headers: `Access-Control-Allow-Origin: http://localhost:8000` (+ `Access-Control-Allow-Credentials: true` if cookies). `*` forbids credentials.
- Non-simple requests (JSON POST, `Authorization`) trigger a preflight `OPTIONS` — server must answer `Access-Control-Allow-Methods/Headers`.
- Cross-origin no-cors fetch produces an opaque response whose status/body are not readable by the page. It has legitimate specialized uses, but does not solve a readable JSON API integration.
- Diagnose in DevTools Network tab: red CORS error + failed preflight = server headers missing, not client code.

## Response bodies (one-shot)
What it means: the body stream can be read only once. Calling `.text()` then `.json()` on the same response throws. `res.clone()` makes a second readable copy when you need to read twice (for example, cache + display).

```js
// const res = await fetch(url);
// console.log(await res.text()); console.log(await res.json()); // THROWS — body already consumed
const res2 = await fetch(url);
const copy = res2.clone(); // read twice via clone (service-worker cache pattern)
```

## JSON rules
What to remember: `JSON.stringify` drops functions and `undefined`, throws on `BigInt` and circular objects, and turns `Date` into an ISO string. `JSON.parse` rebuilds objects — pass a reviver function to turn date strings back into `Date`.

```js
console.log(JSON.stringify({ a: 1, b: undefined, f: () => {} })); // {"a":1} — drops fn/undefined
// console.log(JSON.stringify({ x: 10n })); // TypeError — BigInt not serializable
console.log(JSON.parse('{"a":1}'));
console.log(JSON.stringify({ d: new Date(0) })); // {"d":"1970-01-01T00:00:00.000Z"} — Dates become strings
console.log(JSON.stringify({ a: 1 }, null, 2)); // pretty — for files, not wire
// Reviver: JSON.parse(text, (k, v) => k === 'at' ? new Date(v) : v) — revive ISO dates on load
```

## URL building
What it does: `new URL(...)` plus `searchParams.set()` builds a query string with correct encoding (spaces, `&`, `=`). Reading with `.searchParams.get('q')` decodes it back.

```js
const u = new URL('https://api.example.com/items');
u.searchParams.set('q', 'a b&c'); u.searchParams.set('page', '2');
console.log(u.href); // https://api.example.com/items?q=a+b%26c&page=2 — encoded
console.log(new URL('/users/7', 'https://x.com').pathname); // /users/7
```

## Storage (versioned + cross-tab)
What it does: `save` stringifies and stores, `load` reads and parses (returning a fallback on missing or corrupt data). The key includes a version (`todos.v1`) so you can change the shape later by bumping to `v2`. The `storage` event re-renders when another tab changes the same key.

```js
// localStorage: strings, synchronous and per origin; quotas/availability vary.
// Reads and writes can throw (policy, quota, environment); guard both.
const KEY = 'todos.v1'; // version — bump to invalidate old shapes
const save = (k, v) => localStorage.setItem(k, JSON.stringify(v));
const load = (k, fb) => { try { const s = localStorage.getItem(k); return s ? JSON.parse(s, (kk, vv) => kk === 'at' ? new Date(vv) : vv) : fb; } catch { return fb; } };
// sessionStorage is scoped to a tab/page session. Cookies have several uses;
// browser auth session cookies should be server-set with an explicit security policy.
window.addEventListener('storage', (e) => { if (e.key === KEY) render(load(KEY, [])); }); // cross-tab sync
// Beyond 5MB / structured queries / offline-first → IndexedDB (async, object stores) — pointer only here; localStorage covers this track.
```

## Pitfalls
- Forgetting the `!res.ok` check treats a 404 as success — always throw on non-`ok` status.
- POST without `Content-Type: application/json` means the server can't tell it's JSON — set the header when sending JSON.
- Storing an object directly gives `"[object Object]"` — always `JSON.stringify` on save, `JSON.parse` on load inside `try/catch`.
- `JSON.stringify` on a circular object throws `TypeError: Converting circular structure`.
- `fetch` on `file://` fails — serve over `http://localhost` with `python3 -m http.server`.
- Reading `res.json()` then `res.text()` on the same response throws `Body already consumed` — `clone()` first if you need two reads.
- `mode: 'no-cors'` doesn't fix CORS — it returns an opaque response with no readable body.

## Try it
```bash
node -e 'const u=new URL("https://a.com/x"); u.searchParams.set("q","a b&c"); console.log(u.href)'
node -e 'console.log(JSON.stringify({a:1,b:undefined}), JSON.parse("{\"a\":1}"))'
node --input-type=module -e 'const r=await fetch("https://api.github.com/zen"); console.log(r.ok, r.status, (await r.text()).slice(0,60))'
```

## Optional scratch drills (inside js-dom/work or js-http/work)
1. `url.mjs`: build URL with `q='hello world&x=1'`, `page=2` via `URLSearchParams`; print encoded href; parse back with `new URL(...).searchParams.get`.
2. `get.mjs`: `getJSON()` with `AbortSignal.timeout` + `!ok` check + content-type guard; fetch a JSON endpoint; prove 404 (`https://api.github.com/nope-xyz`) throws your `HTTP 404` error, not silent success. Add `clone()` proof reading `text()` twice via clone.
3. `ship/` (browser over `http://localhost:8000`) — **cached client**: `save/load` with versioned `KEY`, persist todo array across reload, `storage`-event re-render in second tab, `FormData` upload stub, loading/error/empty states. Show `JSON.stringify` dropping `undefined`/functions in console.

## Break it
Serve `ship/` from `:8000` while API runs on `:3000` with no CORS headers — reproduce the CORS block in DevTools Network. Add `Access-Control-Allow-Origin: http://localhost:8000` server-side (see [[11-js-node-http]]), re-run green. Log `CORS-blocked → missing-allow-origin → server-header-fix` in [[90-js-protips]].

## Check
1. Which HTTP statuses reject `fetch`, and what must you check manually?
2. Why can't the client "fix" CORS with flags?
3. `localStorage` limits + why version the key?
Gate: distinguish a local HTTP error from connection failure and from a deliberately expired application deadline. A stopped server can reject immediately with a network error; it does not necessarily demonstrate timeout/abort. Use the bundled local fixtures and browser checklist rather than depending on a public endpoint's behavior.

## Related

- [[07-js-async-event-loop|Async & Event Loop]]
- [[08-js-dom-events|DOM & Events]]
- [[11-js-node-http|Node HTTP]]

Sources: [MDN fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch), [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS), [Web Storage](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API), [Fetch standard](https://fetch.spec.whatwg.org/). The helper shown intentionally requires application/json; structured +json types need an explicit broader contract. Lab verification: [[implementation-status]].
