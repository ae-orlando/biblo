---
created: 2026-10-08
updated: 2026-10-08
---


# Original JavaScript track guide — historical reference

Archived on 2026-10-20. Follow [[00-js-how-to-use]] for current prerequisites, lab paths and assessment. Earlier environment-verification claims below are historical, not a new execution record.

Self-contained JavaScript-as-a-language course. No framework needed. Separate from tooling (Vite/React/Tailwind parked until Phase 5) — this is the *language itself* plus the browser + Node runtimes for Phases 0-4.

## Order (each builds on the last)

| # | Note | What you gain | You ship | Phase |
|---|---|---|---|---|
| 01 | [[01-js-values-types\|Values & Types]] | primitives, `===` vs `==`, coercion, operators | `type-inspector` CLI | 0 |
| 02 | [[02-js-control-flow\|Control Flow]] | truthiness, `if/switch/for/while` | `fizz` + `menu` CLI | 0 |
| 03 | [[03-js-functions-scope\|Functions & Scope]] | declarations, arrows, hoisting, closures | `adder/counter` module | 0 |
| 04 | [[04-js-objects-prototypes\|Objects & Prototypes]] | literals, `this`, prototypes, classes | `user` class + proto chain | 0-1 |
| 05 | [[05-js-arrays-iterables\|Arrays & Iterables]] | methods, `Map/Set`, iteration | `stats/dedupe/group` on data | 0-1 |
| 14 | [[14-js-strings-numbers-dates\|Strings, Numbers, Dates]] | string methods, `Math`, `Date`, `Intl` | `parse/format` CLI | 0-1 |
| 06 | [[06-js-destructuring-modules\|Destructuring & Modules]] | spread/rest, ESM `import/export` | plugin loader | 2 |
| 07 | [[07-js-async-event-loop\|Async & Event Loop]] | event loop, promises, `async/await` | timed `delay-race` demo | 1-3 |
| 08 | [[08-js-dom-events\|DOM & Events]] | select, manipulate, events, forms | validated todo page | 1 |
| 09 | [[09-js-fetch-storage\|Fetch & Storage]] | `fetch`, JSON, `localStorage`, URL | cached API client page | 1-3 |
| 10 | [[10-js-node-scripts\|Node Scripts]] | `fs`, `argv`, `npm`, ESM in Node | `cat/upper/args` CLIs | 2 |
| 11 | [[11-js-node-http\|Node HTTP]] | `node:http` server, JSON API + CORS | todos API + `curl` proofs | 3 |
| 12 | [[12-js-errors-regex\|Errors & Regex]] | `try/catch`, `Error`, regex, debugging | validator + `HttpError` mapping | 0-4 |
| 13 | [[13-js-capstone\|Capstone]] | spec: CLI + page + server using everything | full todo system | 4 |
| 90 | [[90-js-protips\|JS Protips]] | gotcha log, append as you bleed | always | always |

## How to study each note (mastery loop, ~60-90 min)

Every note follows the same 5-step loop. Don't skip steps — reading without building doesn't stick.

1. **Read** the concept (10 min). Note the `Outcomes` box at the top of each note.
2. **Try it** — run every `Try it` block by hand, first in Chrome DevTools console (`Ctrl+Shift+J`) for DOM notes, then in Node. Verified on `node v24.21.0` here.
3. **Build it** — guided mini-build (spec in note). Files land in `03-exercises/js-lang/NN-topic/` as `.mjs` (or `.html`/`.js` for DOM notes).
4. **Break it** — each note has a `Break it` bug to reproduce + fix. Log the cause in [[90-js-protips]].
5. **Ship it + Check** — independent mini-app + 3 self-check questions. Gate before moving on: `node --check` clean, acceptance commands pass, and you can explain the output without re-running.

```bash
mkdir -p ~/learning/js/03-functions
cd ~/learning/js/03-functions
node --check ex1.mjs && node ex1.mjs
```

Scratch patterns:
```bash
node scratch.mjs        # run file
node -e 'console.log(typeof null)'  # one-liner
node --watch scratch.mjs # rerun on save (Node 20+)
node                    # REPL, Ctrl+D to exit
```

## Setup (once)

```bash
fnm install --lts
fnm default lts-latest
fnm use lts-latest
node -v  # v24.21.0 here
npm -v
which node  # must point to fnm shims, not /usr/bin/node
```

VSCode: plain `.mjs` file + integrated terminal. Chrome: console + Network tab for DOM/fetch notes (08-09). No bundler, no TS until Phase 5.

## Rules

- `const` by default, `let` to reassign, never `var` in new code (see [[01-js-values-types]]).
- `===` always; `==` only when you can explain the coercion.
- One `await` chain per function, always handle rejection (see [[07-js-async-event-loop]]).
- Code lives in `~/learning/js/`. Obsidian holds concepts (`02-notes/05-javascript-language/`), exercises land in `03-exercises/js-lang/`. No per-exercise Obsidian notes.
- Reference: MDN JS Guide + Reference. This track teaches you to *read* MDN + ECMA-262, not replace it.
- Compat: if a method is ES2023+, check MDN compat table / `caniuse` before relying on it in browser code. Node v24 here supports all methods used in this track.
- Log every bleed in [[90-js-protips]] as `symptom → cause → fix`. The note's `Break it` section tells you what to log.

## Workflow for web dev (standard)

Always serve over `http://localhost`, never `file://` (modules + `fetch` + CORS need it):

1. Prototype in console (`document.querySelector`, `fetch`).
2. Promote to `~/learning/js/NN-topic/scratch.mjs`, run with `node` (or `node --watch`).
3. Promote to exercise file in `03-exercises/js-lang/`.
4. For DOM/fetch: one folder per build with `index.html` + `<script type="module" src="./app.js">`, serve with `python3 -m http.server 8000`, open `http://localhost:8000`.
5. For Node: `node script.mjs --flag`, then `node server.mjs` + `curl -i localhost:3000/api/...` (use `-i` to see status + headers).
6. Script loading: plain `<script>` blocks parsing; `<script defer>` runs after parse in order; `<script async>` runs whenever loaded (order not guaranteed); `<script type="module">` defers by default + strict + ESM imports. Use `type="module"` for all builds here.

## Related

- [[00-web-foundations|Web Foundations]] (client/server, HTTP, JSON, ports)
- [[10-node-installation|Node Installation]] (fnm workflow)
- [[90-js-protips|JS Protips]]
- [[13-js-capstone|Capstone]]
