---
created: 2026-10-08
updated: 2026-10-21
---

# JavaScript learning path — language, Node and browser

> For your current fullstack direction, focus on Python/FastAPI first and HTML/CSS before the frontend JavaScript stage. Node CLI/HTTP labs remain useful optional runtime extensions, **not** a requirement to specialize in a second backend framework. A later browser capstone can consume your FastAPI API instead of making Node the product backend. See [[master-plan]].

Use [[baseline-diagnostic]] rather than assuming you are a beginner or already proficient. This is framework-free: Node and a browser expose mechanisms before a project justifies extra tooling. Existing Node 24 is sufficient; do not install a version manager just to begin.

## Sequence

| Unit | Read | Verified practice |
| --- | --- | --- |
| Values and decisions | [[01-js-values-types]], [[02-js-control-flow]], basic functions from [[03-js-functions-scope]], strings/errors from [[14-js-strings-numbers-dates]] and [[12-js-errors-regex]] | `js-values`: strict count parsing |
| Data and identity | Full [[03-js-functions-scope]], [[04-js-objects-prototypes]], [[05-js-arrays-iterables]] | `js-data`: pure aggregation with malformed records and arbitrary keys |
| Modules and Node | [[06-js-destructuring-modules]], [[10-js-node-scripts]], full [[12-js-errors-regex]] | `js-cli`: file report with explicit process contract |
| Asynchronous work | [[07-js-async-event-loop]] | `js-async`: bounded concurrency, stale successes and stale failures |
| HTTP | [[00-web-foundations]], [[11-js-node-http]] | `js-http`: tested CRUD API, bounded byte input and failure responses |
| Browser | [[17-html-css-and-browser-workflow]], [[08-js-dom-events]], [[09-js-fetch-storage]] | `js-dom`: model checks **plus** required browser evidence |
| Integration | [[13-js-capstone]] | Independently integrate and test a changed requirement |

See [[practice-catalog]] for specifications, starter code, behavioral checks and progressive hints. One lab can cover several concepts; its number need not match an older lesson number.

## Practice workflow

From the vault root:

```bash
python3 90-tools/practice.py start js-values
python3 90-tools/practice.py check js-values
```

Edit the created `work/` files. The launcher never overwrites an existing attempt. Short drills in retained lessons are **optional self-authored scratch work**, not promises that the old per-lesson directories already contain files. Put those drills in a related lab's `work/` directory. The linked lab's behavioral contract and [[study-and-review]] supersede syntax-only historical gates.

Use `.mjs` for Node ESM in this course. Browser modules are loaded with `<script type="module">` over loopback HTTP. `.js` can also be ESM when Node's package configuration specifies it; `.mjs` is a simple explicit convention, not the only language option.

## What to do when stuck

Read the actual failing assertion or error and its relevant stack frames. Distinguish syntax, runtime, logic and environment failures. Reduce the reproducer, inspect values and use a debugger when useful—there is no phase at which debugging tools suddenly become legitimate.

Keep a concise symptom → cause → fix → regression entry in [[90-js-protips]] or a dated evidence note. A copied reference passes the reference audit, not your independent checkpoint.

## Assessment

Pass behavioral checks, explain one misconception, show a caught deliberate bug and meet an unfamiliar change request. `node --check` only parses; it does not execute, test outputs or establish mastery. Browser behavior and accessibility are separately observed. Older “verified on version X” labels in archived material are not fresh verification claims; consult [[implementation-status]].

Sources: [MDN JavaScript guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide), [Node 24 documentation](https://nodejs.org/docs/latest-v24.x/api/), [ECMAScript specification](https://tc39.es/ecma262/).
