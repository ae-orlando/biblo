---
created: 2026-10-08
updated: 2026-10-21
---

# 90 — JS Protips (gotcha log)

Append one line per bleed. Format: `date — symptom → cause → fix`. Each `Break it` section in 01-14 tells you what to log here.

## Seed entries

- `==` true but `===` false (`1 == '1'`) → coercion → use `===`; only `x == null` idiom allowed.
- `[10,9].sort()` → `[10,9]` → lexicographic → `sort((a,b)=>a-b)`, or `toSorted` for copy.
- `NaN !== NaN` → IEEE → `Number.isNaN`.
- `typeof null === 'object'` → legacy bug → `x === null`.
- Detached method `const f = o.m; f()` → `this=undefined` → `bind` or `() => o.m()`.
- Arrow as method → captures outer `this` → method shorthand `m() {}`.
- `for...in` on array → string indices + inherited → `for...of`.
- Missing `break` in `switch` → fallthrough → always `break` or comment `// fallthrough`.
- `var` loop + closures → shared binding → `let`.
- `Array(3).map` does nothing → holes → `Array.from({length:3}, (_,i)=>i)`.
- `fetch` 404 doesn't throw → must check `!res.ok`.
- `localStorage` object → `"[object Object]"` → `JSON.stringify`/`parse` + `try/catch`.
- `g`-regex + `.test` flips → `lastIndex` stateful → remove `g` or reset `lastIndex = 0`.
- `new RegExp(input)` crash → metachars → escape: `input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')`.
- `0.1+0.2 !== 0.3` → binary floating point → choose an explicit precision/rounding model; integer minor units still need range checks and Math.round is not a universal financial arithmetic fix.
- Spread copy still shares nested → shallow → `structuredClone` for deep.
- `forEach(async)` not awaited → returns `undefined` → `for...of` or `Promise.all(map)`.
- `require` in `.mjs` → `ReferenceError` → `import` (ESM only here).
- `??` vs `||` defaults swapped (`0` clobbered) → `||` catches any falsy → `??`/`??=` for nullish only.
- `?.` chain returned `undefined` silently → short-circuit → guard before chain or `??` fallback.
- `replace('a','b')` changed one hit → first-only → `replaceAll` or `/g`.
- `Number('')` → `0` surprise → validate empty before converting.
- `getMonth()` off by one → 0-indexed → `+1` for display, ISO for storage.
- `YYYY-MM-DD` shifted a day → date-only parses as UTC → store ISO, display `Intl`.
- Non-ISO parsing varies → specify format and calendar validity; a YYYY-MM-DD regex does not validate leap years or impossible dates.
- `res.json()` twice threw → one-shot body stream → `clone()` before second read.
- CORS blocked with `fetch` TypeError → missing `Access-Control-Allow-Origin` → server header fix (never `no-cors` for APIs).
- `getAttribute('value')` stale → initial HTML vs live → `.value`/`.checked` properties.
- `readFile` dumped `Buffer` → missing encoding → pass `'utf8'`.
- Server crashed on `{bad` POST → unhandled `JSON.parse` → `try/catch` → `400`.
- Static import of a missing ESM export → linking SyntaxError; reading a missing property from a dynamic module namespace is different and can return undefined.
- `sort` mutated state array → in-place → `toSorted/toSpliced/with` for UI state.

## Escape helper (copy)

These helpers are context-limited, not universal sanitizers. Prefer literal string search and DOM textContent where appropriate. Seed entries are instructional examples, not evidence that you personally encountered every issue.

```js
const escRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const escHtml = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
```

## Related

- [[00-js-how-to-use|How to Use]]
- [[12-js-errors-regex|Errors & Regex]]
