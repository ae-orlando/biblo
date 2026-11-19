---
created: 2026-10-08
updated: 2026-10-21
---

# 02 — Control Flow (`if`, `switch`, loops)

> Prerequisite: [[01-js-values-types]]. Practice: `js-values`, followed by `js-data`, in [[practice-catalog]]. Use explicit loops when they make the decision and state clearer; map/filter are not universally superior.

## Outcomes

After this note you can: tell which values count as true/false in an `if`; use `for...of` for list values, `for...in` for object keys, and `while` for repeat-until-done; write a `switch` that doesn't leak into the next case; pick `??` vs `||` for safe defaults.

## Mental model
What happens: `if` runs a branch only when its test passes. But the test is not limited to `true` / `false` — JS treats a fixed set of values as falsy (see note 01) and everything else as truthy. So `if (x)` means "if x is not falsy".
Three loop families: use `for (let i...)` when you count, `for...of` when you want each value in a list, `for...in` when you want each key name in an object (never for arrays), `while` when you repeat until a condition changes. `switch` compares with `===` and keeps running into the next case unless you write `break`.
Chain with `else if`, not nested pyramids.

```js
const x = '2';
if (x === 2) console.log('num');
else if (x === '2') console.log('str-2'); // runs
else console.log('other');
```

## `switch` (strict + fallthrough)
What it does: compares one value against many `case` labels using `===`. Without `break`, it falls through and runs the next case too — that is the #1 switch bug, so end every case with `break` (or group two cases that share one branch).

```js
const cmd = 'start';
switch (cmd) {
  case 'start': console.log('go'); break;
  case 'stop':
  case 'halt': console.log('bye'); break; // shared branch
  default: console.log('?');
}
// No break = falls into next case — the #1 switch bug.
```

## Loops
What each does: `for (let i=0; i<3; i++)` repeats with a counter. `for (const v of list)` gives you each value in order. `for (const k in obj)` gives you each key name. `while` repeats while a condition stays true. `do...while` runs at least once. `break` exits the loop, `continue` skips to the next round.

```js
for (let i = 0; i < 3; i++) process.stdout.write(i + ' '); // 0 1 2 — counted
console.log();
for (const v of ['a', 'b']) console.log('of:', v); // values — arrays, strings, Map/Set
for (const k in { a: 1, b: 2 }) console.log('in:', k); // keys — objects only
let n = 3; while (n > 0) { n--; } // conditional
do { n++; } while (n < 1); // runs at least once
outer: for (let i = 0; i < 2; i++) {
  for (let j = 0; j < 3; j++) {
    if (j === 1) continue;       // skip this j
    if (i === 1) break outer;    // labeled break exits BOTH loops
    console.log(i, j);
  }
}
```

## Ternary + short-circuit (expression style)
What they do: `cond ? a : b` is a one-line `if/else` that returns a value. `??` fills in a default when the value is missing (`null`/`undefined`). `||` fills in a default when the value is any falsy. `a && b` runs `b` only when `a` is truthy — used as a guard.

```js
const age = 20;
console.log(age >= 18 ? 'adult' : 'minor');
const opts = {};
const port = opts.port ?? 3000;   // nullish default
const label = opts.name || 'anon'; // falsy default (careful: 0/'' overridden)
opts.verbose && console.log('v');  // guard: runs only if truthy
```

## Pitfalls
- `if (x = 1)` assigns `1` to `x` instead of comparing — always write `===` for comparison.
- `for...in` on an array gives index strings (`'0'`, `'1'`) plus extra keys — use `for...of` for array values.
- Missing `break` in `switch` runs the next case too — end every case with `break`.
- `while` that never changes its condition loops forever — prefer `for...of` when you iterate a list.
- `continue` inside `while` can skip your increment line at the bottom — `for` keeps the increment in one place, so it's safer for counting.

## Try it
```bash
node -e 'for(const v of [10,20]) console.log(v); for(const k in {a:1}) console.log(k)'
node -e 'let s="start"; switch(s){case "start": console.log("go"); break; default: console.log("?")}'
node -e 'const o={}; console.log(o.port ?? 3000, o.name || "anon")'
```

## Optional scratch drills (inside a related lab's work directory)
1. `fizz.mjs`: 1-30, `Fizz` %3, `Buzz` %5, `FizzBuzz` both. Two versions: `if/else` and ternary (`cond ? a : b`). Arg: max via `process.argv[2] ?? 30` (`process.argv[2]` is the first command-line argument after the filename, always text).
2. `keys.mjs`: given `{a:1,b:2}` + array `['x','y']`, print `for...in` (key names) vs `for...of` (values) results for both. Comment why `for...in` on array is wrong.
3. `ship.mjs` — **menu CLI**: `switch` on `argv[2]` (`start|stop|halt|*`) with shared `stop/halt` branch, `break` every branch, `default` usage line + `process.exitCode = 1` (exit `1` means error). Empty arg prints usage to `stderr` (error output).

## Break it
Comment out one `break` in `ship.mjs` and run `node ship.mjs stop`. Record the fallthrough output, restore the `break`, and log `switch-fallthrough → missing break → always break or // fallthrough` in [[90-js-protips]].

## Check
1. What does `if` actually test — `true`, or something wider?
2. When do you use `for...in` vs `for...of`?
3. `port = opts.port ?? 3000` vs `||`: which clobbers an explicit `0`?
Gate: demonstrate valid zero, malformed text and missing input in `js-values`; explain which branch is taken and why. In scratch CLIs, also assert streams and statuses rather than merely looking at logs.

## Related

- [[01-js-values-types|Values & Types]]
- [[03-js-functions-scope|Functions & Scope]]

Sources: [MDN control flow](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling), [for...of](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of). See [[implementation-status]] for executed checks; retained snippets are not all re-executed.
