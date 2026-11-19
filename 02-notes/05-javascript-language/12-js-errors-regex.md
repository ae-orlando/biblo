---
created: 2026-10-08
updated: 2026-10-21
---

# 12 — Errors & Regex (`try/catch`, debugging)

> Basic error handling is a prerequisite to the first JS lab; return to filesystem/HTTP details later. Practice: `js-values`, `js-cli` and `js-http` in [[practice-catalog]]. Model a failure contract, not a catch-all success fallback.

## Outcomes

After this note you can: tell the three bug kinds apart (typo that stops parsing, crash mid-run, silent wrong answer); write file code that returns a fallback for missing files but rethrows real errors; map server errors to status codes without leaking internals; check text with regex while avoiding the stateful-`g` and injection traps.

## Mental model
What the three families mean: `SyntaxError` means the file never ran (typo — find it with `node --check`). Runtime errors (`TypeError`: wrong shape like `null.foo`, `ReferenceError`: unknown variable, `RangeError`: number out of range) mean it started then crashed — catchable with `try/catch`. Logic bugs throw nothing and look correct — only tests and careful reading catch them.
What `throw` / `try/catch` do: `throw new Error('msg')` stops the current path and jumps to the nearest `catch`. `finally` runs cleanup either way. Always throw `Error` objects (they carry a stack trace); `cause` attaches the original error underneath.
What regex is: a mini-pattern inside `/.../flags` for checking or reshaping text. `test()` asks yes/no, `match()` extracts, `replace()` rewrites.

```js
try {
  JSON.parse('{bad');
} catch (e) {
  console.log(e instanceof SyntaxError, e.message.slice(0, 20)); // true Unexpected token...
}
throw new Error('boom', { cause: { id: 7 } }); // cause chains — log it
```

## `try/catch/finally` + shapes
What each does: `try` runs risky code. `catch (e)` runs if it throws — `e.code` identifies Node I/O failures like `ENOENT` (missing file), `e instanceof TypeError` identifies error kinds. Unknown errors should be rethrown, not swallowed. `finally` runs cleanup (close, clearTimeout) either way. `HttpError` below is a custom error that also carries an HTTP status so the server can answer `400` / `404` / `500`.

```js
async function load(f) {
  try {
    const { default: fs } = await import('node:fs/promises');
    return await fs.readFile(f, 'utf8');
  } catch (e) {
    if (e.code === 'ENOENT') return null; // expected — fallback
    throw e; // unexpected — rethrow, don't swallow
  } finally {
    // cleanup (close, clearTimeout) — runs either way
  }
}
// Custom: class HttpError extends Error { constructor(s, m) { super(m); this.status = s; } }
// API mapping: catch (e) { const status = e.status ?? 500; res.writeHead(status, ...); res.end(JSON.stringify({ error: status === 500 ? 'internal' : e.message })); }
// Client: try { await getJSON() } catch (e) { showError(friendly(e)); } — friendly() maps TypeError/AbortError/HTTP to copy.
```

`catch` without param (`} catch {`) for ignore; `e.code` for Node IO, `e instanceof` for types, `res.ok` for HTTP (not exceptions).

## Debugging workflow (no debugger needed yet)
What each command does: `node --check` only parses for typos without running. `--trace-uncaught` prints the full crash path. `console.log({ user })` prints a labeled object, `console.table` prints arrays as a table, `console.time/timeEnd` measures speed.

```bash
node --check app.mjs   # syntax first
node --trace-uncaught app.mjs  # full stack on throw
node --inspect app.mjs # then chrome://inspect for breakpoints (Phase 4+)
```

```js
console.log({ user }); // { user: {...} } — labeled object log
console.table([{ a: 1 }, { a: 2 }]); // tables for arrays
console.time('x'); /* ... */ console.timeEnd('x'); // timing
// debugger; // breakpoint statement — pauses in DevTools/--inspect
```

## Regex essentials (5 patterns cover 80%)
What each does: `/^\d+$/` means "only digits from start (`^`) to end (`$`)". `i` ignores case, `g` replaces all hits (not just the first). `(?<name>...)` captures a labeled piece into `.groups`. `new RegExp(str)` builds a pattern from a variable — escape user text first or special chars like `.*` become commands.

```js
console.log(/^\d+$/.test('42'), /^\d+$/.test('4a')); // true false — full-number check
console.log('a@b.co'.match(/^[^@\s]+@[^@\s]+\.[^@\s]+$/)?.[0]); // crude email
console.log('2026-10-08'.match(/(?<y>\d{4})-(?<m>\d{2})-(?<d>\d{2})/)?.groups); // {y,m,d} — named groups
console.log('hi  a'.replace(/\s+/g, ' ')); // hi a — g = all
console.log('camelCase'.replace(/[A-Z]/g, (m) => `-${m.toLowerCase()}`)); // camel-case — fn replace
const re = new RegExp(`^${'hi'}.*`, 'i'); // dynamic — escape user parts! (see protips)
// Prefer URL/Intl over regex: new URL(s) for URLs, /^\d+$/ for ints, crude-email only for UX hint (server validates).
```

Flags: `g` all, `i` case-insensitive, `m` `^$` per line, `s` `.` matches newline, `u` unicode, `v` unicode-sets (ES2024).

## Pitfalls
- Empty `catch {}` hides real bugs — always log or rethrow what you didn't expect.
- `JSON.parse` / `fetch().json()` throw on malformed text — wrap in `try/catch` and answer `400`, not `500`.
- A regex with `g` plus `.test()` remembers `lastIndex`, so repeated tests flip `true` then `false` — drop `g` for `test`, or reset `re.lastIndex = 0`.
- `new RegExp(userInput)` treats typed characters like `.*` as commands and can crash — escape with `input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')` or use `.includes()` for plain text.
- `throw 'string'` has no stack trace — always `throw new Error('msg')`.
- Sending `e.stack` to the UI leaks file paths — log the stack, show a friendly message plus retry.

## Try it
```bash
node --check 03-exercises/js-lang/01-values/starter/main.mjs
node -e 'try{JSON.parse("{bad")}catch(e){console.log(e.constructor.name)}'
node -e 'console.log(/^\d+$/.test("42"), "hi  a".replace(/\s+/g," "))'
node -e 'const r=/a/g; console.log(r.test("a"), r.test("a"), r.lastIndex)'
```

## Optional scratch drills (inside a related lab's work directory)
1. `guard.mjs`: `readFile` wrapper returning `null` on `ENOENT`, rethrowing others; `JSON.parse` wrapper returning `{ok,data|error}`; prove with missing vs corrupt file.
2. `ship.mjs` — **http errors**: `HttpError(status,msg)` class; handler mapping `400/404/500` to JSON (500 hides internals); `fetch` client distinguishing `!ok` from network throw with friendly copy for each.
3. `re.mjs`: `isInt`, crude `isEmail`, `parseDate` named-groups, `slugify` via `replace` chains (see [[14-js-strings-numbers-dates]]). Show `g`-`test` `lastIndex` trap then fix.

## Break it
In `re.mjs`, run the `g`-`test` twice in a row and print both results + `lastIndex` — observe true→false. Fix by dropping `g` (or `re.lastIndex = 0`), re-run true→true. Log `g-test-stateful → lastIndex → no-g-for-test` in [[90-js-protips]].

## Check
1. `e.code` vs `instanceof` vs `res.ok` — which for IO, types, HTTP?
2. Why rethrow unknown errors instead of returning `null`?
3. When is regex the wrong tool (URL/email)?
Gate: `guard.mjs` returns `null` on missing, `{ok:false}` on corrupt, throws on `EACCES`-class unknowns.

## Related

- [[02-js-control-flow|Control Flow]]
- [[90-js-protips|JS Protips]] (escape helper, `cause` log)
- [[14-js-strings-numbers-dates|Strings, Numbers, Dates]]

Sources: [MDN Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error), [try/catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch), [regular expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions). A syntactically valid starter still fails behavior checks. Lab verification: [[implementation-status]].
