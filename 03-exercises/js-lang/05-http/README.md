# Lab: a bounded, tested todo API

**ID:** `js-http` · Node 24 · Outcome: implement an HTTP contract including failure behavior.

Prerequisites: [[00-web-foundations]], [[07-js-async-event-loop]], [[10-js-node-scripts]], [[11-js-node-http]], [[12-js-errors-regex]].

## Contract

Export `createServer()` from `work/server.mjs`; return a fresh **unbound** `node:http` server with independent in-memory state. Tests bind an ephemeral loopback port.

| Request | Response |
| --- | --- |
| `GET /api/todos` | `200` JSON array, initially empty |
| `POST /api/todos` | Require JSON `{text: nonblank string}`; `201 {id,text,done:false}`, trimmed text, distinct string IDs |
| `PATCH /api/todos/ID` | Require JSON `{done:boolean}`; `200` updated todo |
| `DELETE /api/todos/ID` | `204`, no body; missing ID → `404` |
| Unknown route / unsupported method | `404` / `405` respectively |

JSON responses need an appropriate Content-Type. Missing/wrong request JSON media type → `415`; malformed JSON/invalid shape → `400`; request body exceeding **1024 bytes**, including multibyte characters, → `413`. Invalid requests must not crash the server or change the list. Do not destroy the socket before a deliberate error response can be sent.

```bash
python3 90-tools/practice.py start js-http
python3 90-tools/practice.py check js-http
```

This is a local, unauthenticated teaching API, **not a deployment-ready service**. Completion: justify IDs, body limits and errors, add one failing regression case, then propose persistence and ownership checks before integrating a real application.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/js-http/explanation.md) · [Node HTTP](https://nodejs.org/docs/latest-v24.x/api/http.html)
