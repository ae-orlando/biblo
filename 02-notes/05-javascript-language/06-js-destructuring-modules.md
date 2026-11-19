---
created: 2026-10-08
updated: 2026-10-21
---

# 06 — Destructuring & Modules (spread/rest, ESM)

> Prerequisites: functions, objects and arrays. Practice: `js-cli` in [[practice-catalog]]. The course uses explicit .mjs files; it does not require a bundler or an npm package for the labs.

## Outcomes

After this note you can: unpack arrays/objects into variables with defaults and renames; share code between files with `import`/`export` (named, default, and lazy `import()`); build a small plugin loader that picks a file by name and loads it only when needed.

## Mental model
What each syntax does: destructuring unpacks values from an array or object into variables in one line. Spread expands a collection into separate pieces. Rest collects separate pieces into one array or object. Same `...` symbol, three jobs — the position tells you which: left of `=` in a declaration collects (rest), inside a call or literal expands (spread). ESM `import` / `export` shares code between files: `export` makes a name available, `import` brings it in.

```js
const [a, , c = 99, ...rest] = [1, 2];
console.log(a, c, rest); // 1 99 [] — skip + default + rest
const { name = 'anon', id: uid } = { id: 7 };
console.log(name, uid); // anon 7 — default + rename
const o = { x: 1, y: 2 };
console.log({ ...o, x: 9 }); // {x:9,y:2} — later wins
```

## Spread vs rest vs args
What each line does: `(...args)` in a function definition collects all arguments into an array called `args`. `f(...arr)` in a call expands the array so each item becomes a separate argument.

```js
const f = (...args) => args; // rest: collects into array
console.log(f(1, 2, 3)); // [1,2,3]
console.log(Math.max(...[4, 1, 9])); // spread: expands into args
const h = (a, b, ...more) => [a, b, more];
console.log(h(1, 2, 3, 4)); // [1,2,[3,4]]
// Swap without temp:
let x = 1, y = 2; [x, y] = [y, x];
console.log(x, y); // 2 1
```

## ESM (`app.mjs` + `lib.mjs`)
What it is: ESM (ECMAScript Modules) is the built-in file-sharing system. One file exports names, another imports them. `default` means the main export (one per file). Named exports are the extra labeled ones. Always include the file extension (`'./lib.mjs'`) in Node, or it throws `ERR_MODULE_NOT_FOUND`.

```js
// lib.mjs
export const PI = 3.14;
export function add(a, b) { return a + b; }
export default function main() { return 'run'; }
// app.mjs
import main, { PI, add as sum } from './lib.mjs';
console.log(PI, sum(1, 2), main());
import * as lib from './lib.mjs'; // namespace
console.log(Object.keys(lib));
const mod = await import('./lib.mjs'); // dynamic — lazy/conditional
```

Rules: `import` must be top-level (or use dynamic `import()`), extension `.mjs` (or `"type":"module"`), `default` one per file, named infinite. Re-export: `export { add } from './lib.mjs'`.

## CommonJS interop (you will meet it)
What it is: CommonJS (`require` / `module.exports`) is the older Node system. This track uses ESM only (`import` / `export` in `.mjs` files). You just need to recognize CommonJS when you see it in older packages.

```js
// cjs.cjs: module.exports = { a: 1 };  require('./cjs.cjs')
// ESM can default-import CJS: import pkg from './cjs.cjs'
// Current Node can require eligible synchronous ESM; modules with top-level await
// are not eligible for that synchronous path. Dynamic import works asynchronously.
// package.json: { "type": "module" } → .js treated as ESM.
```

In this track: always `.mjs`, always ESM. No `require`.

## JSON modules (Node 22+, import attributes)
What it is: lets you import a `.json` file directly as a JS object. The `with { type: 'json' }` part tells Node "treat this file as JSON".

```js
// data.json: { "port": 3000 }
// import cfg from './data.json' with { type: 'json' };
// console.log(cfg.port);
// Old syntax `assert { type: 'json' }` is deprecated — use `with`.
```

## Pitfalls
- `import './lib'` without the extension throws `ERR_MODULE_NOT_FOUND` in Node — always write `'./lib.mjs'`.
- A static named import that the ESM module does not export fails during module linking with a SyntaxError; it does not silently produce undefined. A missing property read from a dynamically imported namespace is a different operation and can produce undefined.
- Unpacking `undefined` with no fallback throws `TypeError` — write `function f({a} = {})` so missing args default to `{}`.
- Rest (`...rest`) must be last in the list; object spread copies only the top level.
- `require` in `.mjs` throws `ReferenceError: require is not defined` — this track uses `import` only.

## Try it
```bash
mkdir -p .practice-runtime/scratch/jsm
cd .practice-runtime/scratch/jsm
printf 'export const PI=3.14; export const add=(a,b)=>a+b; export default ()=> "run";\n' > lib.mjs
node -e "import('./lib.mjs').then(m=>console.log(m.PI, m.add(1,2), m.default()))"
node --check lib.mjs && echo OK
cd ../../..
```

## Optional scratch drills (inside js-cli/work)
1. `swap.mjs`: destructure `process.argv` to get args, swap two vars via `[a,b]=[b,a]`, rename + default `{port=3000,host='localhost'} = JSON.parse(...)`.
2. `lib.mjs` + `use.mjs`: named + default + namespace + dynamic `import()`. Prove live binding: exported `let n` incremented by lib fn is visible to importer.
3. `ship.mjs` — **plugin loader**: barrel `plugins/index.mjs` re-exporting two command modules; consumer imports barrel, picks command by `argv[2]`, lazy-loads the other via `import()`. Show missing-extension error, then fix.

## Break it
Statically import a missing named export from a small ESM library and observe the linking SyntaxError before normal execution. Compare with `(await import('./lib.mjs')).nope`, a property read that returns undefined. Fix the import contract and log the distinction in [[90-js-protips]].

## Check
1. Same `...`: when does it collect vs expand?
2. Why must Node ESM imports include the extension?
3. Static `import` vs dynamic `import()`: when is each required?
Gate: `ship.mjs unknown-cmd` exits `1` with available-commands usage.

## Related

- [[05-js-arrays-iterables|Arrays & Iterables]]
- [[10-js-node-scripts|Node Scripts]]

Sources: [MDN import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import), [Node ESM](https://nodejs.org/docs/latest-v24.x/api/esm.html), [Node require(ESM)](https://nodejs.org/docs/latest-v24.x/api/modules.html#loading-ecmascript-modules-using-require). Lab verification: [[implementation-status]].
