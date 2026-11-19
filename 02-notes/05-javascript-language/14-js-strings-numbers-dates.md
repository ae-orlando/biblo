---
created: 2026-10-08
updated: 2026-10-21
---

# 14 — Strings, Numbers, Dates (`Intl` for web dev)

> Prerequisite: [[01-js-values-types]]. Practice: `js-values` and `js-data` in [[practice-catalog]], followed by the calendar-date change request in [[13-js-capstone]]. HTML escaping is context-dependent; prefer DOM textContent for user text rather than treating a small escape function as a universal sanitizer.

## Outcomes

After this note you can: change text with `trim`/`split`/`slice`/`replaceAll` without regex; convert text to numbers safely (know when `Number()` vs `parseInt` applies); avoid the month-index, timezone-parse, and display traps in `Date`; format money and dates for humans with `Intl`.

## Mental model
What to remember: strings are immutable — methods like `trim()` or `slice()` return a new string, the original never changes. Numbers are all 64-bit floats, so integers are exact only up to `2^53 - 1` and decimals like `0.1` are approximate. A `Date` is just a millisecond count — formatting (`toISOString` for storage, `Intl` for display) decides how it looks. `Intl` is the built-in formatter for humans (money, dates); ISO strings are for storing and sending.

## Strings (the 12 that cover web dev)
What they do: `trim()` strips edge spaces. `includes/startsWith/endsWith` ask yes/no. `split(',')` cuts text into an array, `join(' - ')` glues an array into text. `slice(a,b)` cuts by position (prefer it over `substring`). `at(-1)` reads from the end. `padStart/padEnd` widen to a length. `replace` changes the first hit only, `replaceAll` changes every hit. `normalize()` unifies accented characters before comparing.

```js
const s = '  Hello, Orl!  ';
console.log(s.trim(), s.trim().length); // Hello, Orl! 11
console.log('hello'.includes('ell'), 'hello'.startsWith('he'), 'hello'.endsWith('lo')); // true true true
console.log('a,b,c'.split(','), ['a','b'].join(' - ')); // [a,b,c] a - b
console.log('hello'.slice(1, 4), 'hello'.at(-1)); // ell o — slice over substring; at() for last
console.log('hi'.padStart(4, '0'), 'hi'.padEnd(4, '!')); // 00hi hi!!
console.log('aaa'.replace('a', 'b'), 'aaa'.replaceAll('a', 'b')); // baa bbb — replace() first only!
console.log('Café'.normalize().length); // composed vs decomposed unicode — normalize before compare
```

```js
// tagged template for safe HTML (preview of 08-XSS rule):
const esc = (str) => String(str).replace(/[&<>"']/g, (c) => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]));
const who = '<img src=x onerror=alert(1)>';
console.log(esc(who)); // &lt;img ... — never interpolate raw user input
```

## Numbers (`Math`, parsing, money)
What each does: `parseInt` / `parseFloat` read a number from the start of text and ignore the suffix. `Number()` converts the whole text (but `Number('')` is `0` — validate empty input first). `toFixed(2)` rounds to 2 decimals for display. `toString(16)` renders in hex. Store money as integer cents and divide only for display, otherwise floats drift.

```js
console.log(Number.parseInt('42px', 10), Number.parseFloat('3.14x')); // 42 3.14 — parse* tolerate suffix
console.log(Number(' 42 '), Number('')); // 42 0 — Number() strict-ish, '' → 0 trap!
console.log(Number.isFinite(1/0), Number.isInteger(3.0)); // false true
console.log((3.14159).toFixed(2), (255).toString(16)); // 3.14 ff
console.log(Math.floor(3.9), Math.ceil(3.1), Math.round(3.5), Math.trunc(-3.9)); // 3 4 4 -3
console.log(Math.min(...[3,1,2]), Math.max(...[3,1,2])); // 1 3
console.log(Math.floor(Math.random() * 6) + 1); // 1-6 die — random is [0,1)
// Money: integers in cents, never floats:
console.log((199 + 299) / 100); // 4.98 — store 199/299, divide only to display
console.log(new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(4.98)); // $4.98
```

## Dates (4 traps + `Intl`)
Date constructors use zero-based month indices. ISO date-only strings parse as UTC midnight; date-time strings without an offset are interpreted as local time. A calendar date is not inherently an instant. Date.now reports wall-clock epoch milliseconds and can jump when the clock changes; performance.now is the better monotonic elapsed-time clock. Use explicit zones and formats for interchange/display.

```js
console.log(new Date(2026, 0, 5).getMonth()); // 0 — TRAP 1: months 0-indexed
console.log(new Date('2026-10-08').toISOString()); // 2026-10-08T00:00:00.000Z — TRAP 2: date-only parses as UTC
console.log(new Date('2026-10-08T12:00:00').getHours()); // 12 — datetime-no-zone parses as LOCAL
const d = new Date('2026-10-08T12:00:00Z');
console.log(d.toISOString()); // UTC canonical — store/transfer this
console.log(d.toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' })); // TRAP 3: toString is local — display with Intl
console.log(Date.now()); // wall-clock epoch milliseconds; not a monotonic duration clock
console.log(new Intl.DateTimeFormat('en-GB', { dateStyle: 'full' }).format(d));
// Note: Temporal API replaces Date for new code (MDN: Date is legacy) — same ISO + Intl habits transfer.
```

## Pitfalls
- `replace('a','b')` without `/g` or `replaceAll` changes only the first hit — use `replaceAll` for every hit.
- `Number('')` is `0` but `parseInt('')` is `NaN` — check for empty input before converting.
- `getMonth()` returns `0-11` (`0` = January) and `getDay()` returns `0` for Sunday — add `+1` for display months.
- Date-only `'YYYY-MM-DD'` parses as UTC midnight while full datetime parses as local — mixing them shifts days across timezones; store ISO, display with `Intl`.
- `Math.random()` is not secure randomness — use `crypto.getRandomValues` / `crypto.randomUUID` for ids and tokens.

## Try it
```bash
node -e 'console.log("a,b,c".split(","), "hi".padStart(4,"0"))'
node -e 'console.log(Number.parseInt("42px",10), (3.14159).toFixed(2))'
node -e 'console.log(new Date(2026,0,5).getMonth(), new Date("2026-10-08").toISOString())'
node -e 'console.log(new Intl.NumberFormat("en-US",{style:"currency",currency:"USD"}).format(4.98))'
```

## Optional scratch drills (inside js-values/work)
1. `slug.mjs`: `trim/lowercase/normalize/replaceAll/split/join` chain turning titles into URL slugs. Handle `Café` + extra spaces.
2. `money.mjs`: cents-int arithmetic + `Intl.NumberFormat` display. Prove `0.1+0.2` display bug and cents fix.
3. `ship.mjs` — **parse/format CLI**: `node ship.mjs "2026-10-08" 499` prints `{ iso, pretty, money }` where `iso` is UTC ISO, `pretty` is `Intl` long date, `money` is USD of cents. Bad date → `stderr` + exit `1`.

## Break it
Compare non-ISO parsing with an explicit YYYY-MM-DD contract. A digits-and-dashes regex only validates shape, not calendar validity: dates such as February 31 need additional validation/round-trip checks or an appropriate calendar API. Record the distinction and test leap years rather than relying on normalization.

## Check
1. `slice` vs `substring` — which do you default to and why?
2. Where do you store money math, and where does `Intl` appear?
3. Date-only vs datetime parse: which is UTC, which is local?
Gate: `slug.mjs` handles `Café  Au  Lait` → `cafe-au-lait`.

## Related

- [[01-js-values-types|Values & Types]]
- [[12-js-errors-regex|Errors & Regex]] (validation + slug regex)
- [[09-js-fetch-storage|Fetch & Storage]] (ISO dates over JSON)

Sources: [MDN Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date), [Intl](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl), [performance.now](https://developer.mozilla.org/en-US/docs/Web/API/Performance/now). Check Temporal/runtime compatibility before choosing it; the labs do not require it. Lab verification: [[implementation-status]].
