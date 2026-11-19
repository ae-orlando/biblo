---
created: 2026-10-08
updated: 2026-10-21
---

# 11 — Node HTTP (JSON API with `node:http`, no framework)

> Prerequisites: [[00-web-foundations]], async, Node scripts and errors. Practice: `js-http` in [[practice-catalog]]. Snippets below illustrate pieces, not one complete verified server; the lab defines a consistent runnable contract and tests. Never expose this unauthenticated teaching server beyond loopback.

## Outcomes

After this note you can: serve a page + JSON API from one Node server with no framework; check POST bodies (size limit, valid JSON, required fields) and answer `400` on bad input; add cross-site permission headers when needed and prove status codes with `curl -i` (shows headers + status).

## Mental model
What the server does: `http.createServer((req, res) =>)` starts a program that waits for requests. For each request you get `req` (what was asked: method + path) and `res` (what you send back: status + headers + body). Node gives you no router, no body parser, no JSON helper — you write those in ~40 lines. That boilerplate is the point: later frameworks just remove it. Serving the page and the API from the same server (same origin) avoids CORS problems in dev.

```js
// server.mjs
import http from 'node:http';
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (req.method === 'GET' && url.pathname === '/api/hello') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ hi: 'world' }));
    return;
  }
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'not found' }));
});
server.listen(3000, '127.0.0.1', () => console.log('http://127.0.0.1:3000/api/hello'));
```

```bash
node server.mjs & sleep 0.5; curl -s localhost:3000/api/hello; kill %1
```

## Reading a JSON body (POST)

The simplified sketch below is intentionally incomplete: string length is not byte length, destroying a socket can prevent an error response, and decoding chunks separately can split multibyte characters. Do not use it as the lab implementation. Retain bounded Buffer chunks, handle stream errors/aborts and decode after complete collection as taught by the lab contract.
What happens: POST data arrives in pieces (`data` events). You glue the pieces into a string, cap the size so a giant upload can't crash you, wait for `end`, then `JSON.parse` it. Malformed JSON throws, so wrap it in `try/catch` and answer `400`.

```js
const body = await new Promise((resolve, reject) => {
  let s = '';
  req.on('data', (c) => { s += c; if (s.length > 1e6) { req.destroy(); reject(new Error('too big')); } });
  req.on('end', () => resolve(s));
  req.on('error', reject);
});
const data = body ? JSON.parse(body) : {};
// Always cap size + try/catch JSON.parse — malformed JSON throws.
```

Full POST route:
```js
if (req.method === 'POST' && url.pathname === '/api/todos') {
  try {
    const data = JSON.parse(await readBody(req));
    if (typeof data.text !== 'string' || !data.text.trim()) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ error: 'text required' }));
    }
    res.writeHead(201, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ id: 1, text: data.text.trim() }));
  } catch {
    res.writeHead(400, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ error: 'invalid JSON' }));
  }
}
```

## Method + route table (tiny router) + static page
What it does: builds a `Map` keyed by `"METHOD /path"` so each route is a small function. Look up the incoming method + pathname, call the match, answer `404` JSON when nothing matches. `GET /` reads `index.html` from disk and serves it as `text/html`.

```js
const routes = new Map([
  ['GET /api/todos', (req, res, url) => listTodos(res)],
  ['POST /api/todos', (req, res, url) => createTodo(req, res)],
]);
const handler = routes.get(`${req.method} ${new URL(req.url, 'http://x').pathname}`);
if (!handler) { res.writeHead(404, ...); return res.end(...); }
await handler(req, res, url);
// GET / → readFile index.html, Content-Type: text/html — same-origin page kills CORS issues in dev.
```

## CORS headers (when cross-origin is required)
What they do: these response headers tell the browser "this API trusts that page origin". Preflight `OPTIONS` is the browser asking permission before a JSON POST — answer `204` with the allow-headers and stop there.

```js
// Allow page http://localhost:8000 to call API :3000:
const ALLOW = 'http://localhost:8000';
res.setHeader('Access-Control-Allow-Origin', ALLOW);
res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); } // preflight short-circuit
// With credentials: also 'Access-Control-Allow-Credentials: true' and never '*' as origin.
```

## Pitfalls
- Forgetting `Content-Type: application/json` on the response leaves clients guessing — always set it for JSON.
- Forgetting `return` after `res.end(...)` lets code fall through and call `res.end` twice, throwing `ERR_STREAM_WRITE_AFTER_END`.
- Ordinary origin-form requests use a path/query, but HTTP has other request-target forms. Parse against a controlled base and validate supported targets; do not trust a Host header as an authorization boundary.
- `JSON.parse` on malformed bodies throws and crashes the server unless wrapped in `try/catch` that answers `400`.
- curl normally exits zero for a completed HTTP exchange even on 404. `-i` displays status but does not assert it. Use an explicit status assertion or an appropriate --fail/--fail-with-body policy; fetch needs a res.ok/status check.
- `Access-Control-Allow-Origin: *` plus cookies/credentials is rejected by the browser — echo the exact page origin instead.

## Try it
```bash
python3 90-tools/practice.py check js-http
node -e 'console.log(new URL("/a?q=1", "http://x").pathname)'
```

## Optional scratch drills (inside js-http/work)
1. `server.mjs`: `GET /api/hello` → `{hi}` + 404 JSON fallback + `GET /` serving `index.html`. Test with `curl -i` showing `200` vs `404` + `Content-Type`.
2. `ship.mjs` — **todos API**: in-memory `[]`; `GET /api/todos` lists, `POST /api/todos` validates `{text:string non-empty}` → `201 {id,text}` else `400 {error}`; body cap + invalid-JSON `400`; CORS block (origin constant + `OPTIONS` 204). `curl -i` proofs for 201/400/404/OPTIONS.
3. `client.mjs`: distinguish an HTTP error response, a stopped server's connection failure and a separately simulated deadline expiry. Assert the class of failure rather than calling every failure a timeout.

## Break it
In the isolated HTTP lab, send malformed JSON and an oversized multibyte body: expect 400 and 413 respectively, with the process still usable. Deliberately remove one guard, observe a failing regression, then restore it. Do not conflate every body/stream failure with invalid JSON or destroy the socket before sending a deliberate response.

## Check
1. Why `return` after every `res.end`?
2. What answers the preflight, and with which headers?
3. `curl` exit 0 on 404 — how do you actually assert status?
Gate: `curl -i` shows `201` + `application/json` on valid POST, `400` on `{}` and on malformed JSON.

## Related

- [[00-web-foundations|Web Foundations]] (HTTP, status codes)
- [[09-js-fetch-storage|Fetch & Storage]]
- [[07-js-async-event-loop|Async & Event Loop]]

Sources: [Node HTTP](https://nodejs.org/docs/latest-v24.x/api/http.html), [WHATWG URL](https://url.spec.whatwg.org/), [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP). The bundled lab uses ephemeral loopback ports and deliberate teardown rather than fixed sleeps/job specs. Lab verification: [[implementation-status]].
