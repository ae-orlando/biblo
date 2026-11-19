---
created: 2026-10-08
updated: 2026-10-08
---

# Original JavaScript capstone — historical reference

Archived on 2026-10-20. The timestamp-ID, serving/route and browser synchronization contracts below are superseded by [[13-js-capstone]]. Preserve this as an earlier design, not a runnable current specification.

## Outcomes

You prove Phases 0-3 without magic: one shared pure logic module used by a CLI, a browser page, and a `node:http` API — with loading/error/empty states, validation, and a11y. All ESM `.mjs`, `node --check` clean, no Vite/Express.

## Goal
Prove Phases 0-3 without magic: one shared logic module used by a CLI, a browser page, and a `node:http` API. All ESM `.mjs`, `node --check` clean, no Vite/Express.

## Spec (`03-exercises/js-lang/13-capstone/`)

```
13-capstone/
  logic.mjs   # pure: parse/validate/format todos, no fs/DOM/http
  logic.test.mjs # node:test: makeTodo/toggle/filter edge cases
  cli.mjs     # node cli.mjs add "buy milk" | list — fs persists todos.json
  server.mjs  # GET/POST /api/todos (port 3000, node:http only) + GET / page
  index.html  # input+list, fetch() to server, textContent only
  app.js      # DOM + fetch, event delegation, stale-guard
```

`logic.mjs` contract:
```js
export const makeTodo = (text) => {
  if (typeof text !== 'string' || !text.trim()) throw new Error('text required');
  return { id: Date.now().toString(36), text: text.trim(), done: false };
};
export const toggle = (t) => ({ ...t, done: !t.done });
export const visible = (todos, q) => q ? todos.filter((t) => t.text.toLowerCase().includes(q.toLowerCase())) : todos;
```

- `cli.mjs`: `readFile`/`writeFile` `todos.json` (`[]` if `ENOENT`), commands via `argv[2]`, usage to `stderr` + `exitCode 1` on misuse. `--help` included.
- `server.mjs`: routes from [[11-js-node-http]] + `readBody` cap + `201/400/404` JSON + CORS block. Serve `index.html` from the same server (`GET /` → `readFile index.html`, `Content-Type: text/html`) to stay same-origin in dev.
- `index.html/app.js`: form `submit` + `preventDefault` + `checkValidity/reportValidity` + `FormData`, `fetch` `getJSON` from [[09-js-fetch-storage]] with `!ok` check + `AbortSignal.timeout`, `render()` with `createElement`/`textContent` + `DocumentFragment`, delegation for toggle/delete, stale-guard on search input (debounced 200ms).
- UI states (required, not bonus): `loading` (disabled form + "Loading…"), `empty` ("No todos — add one"), `error` (`aria-live` message + Retry button). A11y: `<label>`, focus back to input after add, Escape clears search.

## Acceptance

```bash
cd "/home/orlando/Documents/Notes/03-exercises/js-lang/13-capstone"
node --check logic.mjs && node --check cli.mjs && node --check server.mjs && echo CHECK-OK
node --test logic.test.mjs
node cli.mjs add "buy milk" && node cli.mjs list
node server.mjs & SRV=$!; sleep 0.5
curl -s localhost:3000/api/todos
curl -s -X POST localhost:3000/api/todos -H 'Content-Type: application/json' -d '{"text":"web"}'
curl -s localhost:3000/api/todos
curl -s -X POST localhost:3000/api/todos -H 'Content-Type: application/json' -d '{}' # → 400 {error}
curl -s -X POST localhost:3000/api/todos -H 'Content-Type: application/json' -d '{bad' # → 400 invalid JSON
kill $SRV
# browser: node server.mjs, open http://localhost:3000/, add/toggle items, reload persists (server file)
# browser breaks: offline/throttled network shows error+Retry; empty search shows empty-state; two tabs stay in sync via storage event (if local fallback enabled)
```

Explain blind: event-loop order in `app.js`, why `fetch` needs `!ok`, where `this` appears (none in pure logic — why), prototype of a todo (`Object.prototype`), why page + API share one origin in dev and which headers cross-origin would need.

## Related
- [[00-js-how-to-use|How to Use]]
- [[11-js-node-http|Node HTTP]]
- [[08-js-dom-events|DOM & Events]]

Sources: synthesis of 01-12 + 14; MDN + Node docs as cited per note.
