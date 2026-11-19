---
created: 2026-10-08
updated: 2026-10-21
---

# 01 — Values & Types (`typeof`, `===`, coercion)

> Practice: `js-values` in [[practice-catalog]]. Read the basic function, error and string sections listed in its prerequisites first. Older short programs below are optional self-authored drills inside your lab's `work/`, not pre-existing exercise assets.

## Outcomes

After this note you can: name the common value types from memory; use `typeof` to ask for a value's type; use `===` for safe comparison and know the one safe use of `==` (checking `null`/`undefined`); set safe defaults with `?.` (safe property read), `??` (fallback for missing), `||` (fallback for falsy).

## Mental model
What this note covers: every value in JS has a type — a label that tells JS what you can do with it. `typeof` asks for that label. `===` checks if two values are exactly the same.

Types you will use daily: `string` (text in `'quotes'`), `number` (any number like `42` or `3.14`), `boolean` (`true` / `false`), `undefined` (declared but no value assigned yet), `null` (you intentionally left it empty), `object` (a collection — this includes arrays `[]` and plain objects `{}`). Two rare ones to just recognize by name: `bigint` (huge integers with `n` suffix), `symbol` (unique IDs).
Two copying rules: primitives copy the value itself. Objects share a link — two variables can point at the same object, so changing one changes what the other sees.
Two quirks to memorize: `typeof null` says `'object'`. This is a historic mistake in the language — always test null with `x === null`. And `const` locks the variable name, not the contents: `const o = {}` still lets you do `o.k = 1`.

```js
const s = 'hi', n = 42, b = true, u = undefined, z = null;
console.log(typeof s, typeof n, typeof b, typeof u, typeof z);
// string number boolean undefined object  <- null lies
console.log(typeof {}, typeof [], typeof (() => {}));
// object object function  <- arrays are objects, functions are callable objects
```

## `let` / `const` / `var`
What they do: they create a variable (a named slot that holds a value). `const` means you cannot reassign the name later. `let` means you can. `var` is the old version — it leaks out of blocks, so never use it in new code.

```js
const PI = 3.14;       // cannot reassign
let count = 0; count++; // reassignable
// var: function-scoped, hoisted, allows redeclare — never use in new code
{
  let a = 1; const c = 2; var v = 3;
}
console.log(typeof v); // number — var leaked out of block
// console.log(a); // ReferenceError
```

## `===` vs `==` (the single most important rule)
What they do: both compare two values. `===` (strict) checks without converting types — use this. `==` (loose) converts types first, which causes surprises — avoid it, with one exception below.

```js
console.log(1 === '1');  // false — no coercion, use this
console.log(1 == '1');   // true — coerces, avoid
console.log(0 == false, '' == false, null == undefined);
// true true true — the only == case with a use: x == null checks null|undefined
// (x) => ... is a short function: takes x, returns the check result
const isMissing = (x) => x == null; // true for null AND undefined only
console.log(isMissing(null), isMissing(undefined), isMissing(0)); // true true false
console.log(NaN === NaN); // false — NaN never equals itself
console.log(Number.isNaN(NaN), Number.isNaN('x')); // true false (global isNaN coerces, avoid it)
console.log(Object.is(-0, 0), -0 === 0); // false true — edge case
```

## Coercion (explicit beats implicit)
What it is: coercion means JS automatically converts a value from one type to another. Example: `'5' + 1` becomes `'51'` because `+` with text glues strings together. Rule: convert yourself with `Number()`, `String()`, `Boolean()` so there are no surprises.

```js
console.log('5' + 1);   // '51' — + with string concatenates
console.log('5' - 1);   // 4 — - always numeric
console.log(Number('42'), String(42), Boolean(0), Boolean('x'));
// 42 '42' false true
console.log(!!'');      // false — !! forces boolean
console.log(+'42', +'  '); // 42 0 — unary + is Number()
console.log(null ?? 'dflt', undefined ?? 'dflt', 0 ?? 'dflt'); // dflt dflt 0 — ?? only null|undefined
console.log(0 || 'dflt', '' || 'dflt', 'a' || 'dflt'); // dflt dflt a — || any falsy
```

Falsy list (memorize): `false, 0, -0, 0n, '', null, undefined, NaN`. Everything else truthy — including `[]` and `{}`.

## `?.` + logical assignment (defaults without pyramids)
What they do: `?.` (optional chaining) safely reads a property that might not exist — returns `undefined` instead of crashing. `??` (nullish coalescing) picks a fallback only when the left side is `null` or `undefined`. `||` picks a fallback for any falsy value (`0`, `''`, `false` too). `??=` / `||=` / `&&=` are shortcuts that assign only when the condition matches.

```js
const user = { profile: { name: 'orl' } };
console.log(user.profile?.name, user.missing?.name); // orl undefined — no throw
console.log(user.settings?.theme ?? 'light'); // light — ?. + ?? is the standard defaults chain

const opts = {};
opts.port ??= 3000;   // assign only if null|undefined
opts.name ||= 'anon'; // assign if any falsy (careful: 0/'' overridden)
opts.verbose &&= true; // assign only if already truthy
console.log(opts); // { port: 3000, name: 'anon' }
```

Rule: `??`/`??=` for missing values, `||`/`||=` for any-falsy fallbacks, `?.` before any possibly-missing hop.

## Numbers, BigInt, strings, template literals
What they are: `number` covers all normal numbers but cannot exactly represent some decimals (`0.1 + 0.2`). `BigInt` (`10n`) is for integers beyond `Number.MAX_SAFE_INTEGER`. A template literal (backticks `` `hi ${name}` ``) builds text with embedded expressions inside `${}`.

```js
console.log(0.1 + 0.2);              // 0.30000000000000004 — binary float
console.log(Number.MAX_SAFE_INTEGER); // 9007199254740991 — beyond this use BigInt
console.log(10n + 5n);               // 15n — BigInt, no mixing with Number
// console.log(10n + 1); // TypeError: Cannot mix BigInt and other types
const name = 'orl';
console.log(`hi ${name}, ${1 + 2}`); // hi orl, 3 — template literal
console.log('a\nb'.length, '😀'.length); // 3 2 — UTF-16 units, emoji is 2
```

String/number method depth (`slice/split/parseInt/toFixed`, `Date`) lives in [[14-js-strings-numbers-dates]] — this note is operators and identity.

## Pitfalls
- `typeof null === 'object'` — check `x === null` first.
- `NaN === NaN` is false — use `Number.isNaN` to test for `NaN`.
- `0.1 + 0.2 !== 0.3` — decimals are approximate; store money as integer cents and divide only to display.
- `+` glues text if either side is a string — wrap math in `Number()` first.
- `const obj = {}; obj.k = 1` is legal — `const` locks the variable name, not the object contents (use `Object.freeze` to lock top-level keys).
- `a?.b?.c` gives `undefined` as soon as one hop is missing — don't mix with `||` when `0`/`''` are valid values (use `??` so only `null`/`undefined` trigger the fallback).

## Try it
```bash
node -e 'console.log(typeof null, typeof [], typeof (()=>{}))'
node -e 'console.log(1==="1", 1=="1", null==undefined, NaN===NaN)'
node -e 'console.log("5"+1, "5"-1, !!"", 0 ?? "d", "" || "d")'
node -e 'console.log(0.1+0.2, 10n+5n, `hi ${1+2}`)'
node -e 'const o={}; o.p ??= 3000; console.log(o, {a:{}} .a?.b ?? "miss")'
```

## Build it (`03-exercises/js-lang/01-values/`)
1. `eq.mjs`: print table of `===` vs `==` for pairs `(1,'1')`, `(0,false)`, `('',false)`, `(null,undefined)`, `(NaN,NaN)`. Add `Number.isNaN` and `x == null` helper demos.
2. `coerce.mjs`: compare Number, parseInt and complete-string validation on `''`, `' 42 '`, `'42px'` and `'9007199254740992'`. Predict which conversions accept more than the intended count contract; then implement the actual `js-values` lab.
## Break it
`falsy.mjs`: predict Boolean(v) and `v ?? 'fallback'` for `[false,0,-0,0n,'',null,undefined,NaN,[],{}]`. Replace ?? with || and identify every changed non-nullish falsy case, not just two rows. Explain why truthiness cannot validate a count and log one reproduced misconception in [[90-js-protips]].

## Check
1. Why does `typeof null` lie, and what do you write instead?
2. When is `x == null` acceptable and what does it catch?

3. `opts.timeout ??= 5000` vs `||=`: which preserves an explicit `0`? Why?
Gate: pass `js-values`, explain its TypeError versus RangeError contract, and show that a permissive parseInt implementation fails a regression case. Syntax checks alone are insufficient.

## Related

- [[00-js-how-to-use|How to Use]]
- [[02-js-control-flow|Control Flow]]
- [[14-js-strings-numbers-dates|Strings, Numbers, Dates]]

Sources: [MDN data structures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures), [equality comparisons](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness), [ECMAScript](https://tc39.es/ecma262/). Executed lab checks are recorded in [[implementation-status]].
