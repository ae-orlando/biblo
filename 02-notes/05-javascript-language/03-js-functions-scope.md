---
created: 2026-10-08
updated: 2026-10-21
---

# 03 — Functions & Scope (declarations, arrows, closures)

> Prerequisite: [[02-js-control-flow]]. Practice: `js-values` for functions, `js-data` for transformations and `js-async` for closure-local state. See [[practice-catalog]].

## Outcomes

After this note you can: write the three function forms (declaration, expression, arrow) and know when each runs; explain TDZ as "using a `let`/`const` before its line throws"; write a function that remembers private state (closure); use `map`/`filter`/`reduce` instead of most `for` loops.

## Mental model
What a function is: a named block of reusable code. You call it with inputs (arguments), it runs, it optionally returns an output with `return`.
Four ways to write one: `function name(){}` (a declaration — usable before its line), `const f = function(){}` (an expression — usable only after its line), `const f = () =>` (arrow — short form for callbacks, has no own `this`), `method(){}` inside an object (shorthand for object actions).
What scope is: where a variable is visible. A block `{ ... }` with `let`/`const` keeps variables inside. Each function call gets fresh variables.
What a closure is: when a returned inner function remembers the variables from the call that created it, even after that call finished. That is how private state works.
Prefer pure functions: same input always gives same output, and they don't change outside variables — easier to test.

```js
greet('orl'); // works — declarations hoist
function greet(n) { return `hi ${n}`; }

const add = (a, b = 0) => a + b; // default param, implicit return
console.log(add(2), add(2, 3));   // 2 5
const nums = [1, 2, 3];
console.log(nums.map((x) => x * 2)); // [2,4,6] — arrows as callbacks
```

## Params: defaults, rest, spread
What they do: a default (`a = 1`) fills in the value when the caller omits it. Rest (`...rest`) collects extra arguments into an array. Spread (`...arr`) expands an array into separate arguments.

```js
function f(a = 1, ...rest) { return [a, rest]; }
console.log(f(), f(9, 8, 7)); // [1,[]] [9,[8,7]]
console.log(Math.max(...[1, 9, 3])); // 9 — spread calls, rest collects
function g({ name = 'anon', id } = {}) { return `${name}:${id}`; }
console.log(g({ id: 7 }), g()); // anon:7 anon:undefined — destructured param with fallback
```

## Scope + hoisting
What it means: hoisting is JS reading declarations before running code. A `function` declaration can be called before its line. `let`/`const` are also seen early but blocked until their line runs — that blocked zone is called the TDZ (Temporal Dead Zone) and touching it throws `ReferenceError`. `var` gives `undefined` instead — one reason to avoid it.

```js
// var hoists (undefined), let/const hoist to TDZ (ReferenceError until init)
console.log(typeof fnDecl); // function — hoisted
function fnDecl() {}
// console.log(x); // ReferenceError: Cannot access 'x' before initialization
let x = 1;
{
  let y = 2; const z = 3;
  console.log(x, y, z); // 1 2 3 — inner sees outer
}
// console.log(y); // ReferenceError — block-scoped
```

## Closures (the single most important JS idea)
What it is: a function that keeps access to the variables where it was created, after the outer function returned. Below, each `counter()` call creates a fresh `n`, and the returned arrow keeps its own `n` alive.

```js
function counter() {
  let n = 0; // private — only the returned fn sees it
  return () => ++n;
}
const c1 = counter(), c2 = counter();
console.log(c1(), c1(), c2()); // 1 2 1 — independent states
// Loop trap: var shares one binding, let gives one per iteration
const fns = [];
for (let i = 0; i < 3; i++) fns.push(() => i);
console.log(fns.map((f) => f())); // [0,1,2] — with var this would be [3,3,3]
```

## `this` preview (full rules in Objects note)
What `this` is: inside a method, `this` means "the object before the dot" (`o.hi()` → `this` is `o`). Arrow functions don't get their own `this` — they use the surrounding one, so don't use arrows as object methods.

```js
const o = {
  name: 'orl',
  hi() { return `hi ${this.name}`; },          // method: this = o
  bye: () => `bye ${this.name}`,              // arrow: this = outer (undefined in module)
};
console.log(o.hi()); // hi orl
// Rule of thumb: use method shorthand for methods, arrows for callbacks.
```

## Higher-order (map/filter/reduce replace most loops)
What they do: higher-order means a function that takes another function. `arr.map(fn)` builds a new array by transforming each item. `arr.filter(fn)` keeps only items where `fn` returns true. `arr.reduce(fn, start)` boils the array down to one value.

```js
const xs = [1, 2, 3, 4];
console.log(xs.filter((x) => x % 2 === 0).map((x) => x * 10)); // [20,40]
console.log(xs.reduce((sum, x) => sum + x, 0)); // 10
```

## Pitfalls
- Calling `const f = () => ...` before its line throws `ReferenceError` (it lives in the TDZ until its line runs) — only `function name(){}` can be called early.
- Arrow as object method uses the surrounding `this`, not the object — write methods as `hi() {}`.
- Arrows have no own arguments binding; a reference can resolve to an enclosing function's arguments. Use rest parameters when the arrow needs its own inputs.
- `var` in a loop shares one variable across all pushed callbacks — use `let` so each round gets its own.
- Destructuring a possibly-missing argument needs a fallback like `= {}` or it throws `TypeError` on `undefined`.
- Changing outside variables inside `map` defeats its purpose — return new values instead.

## Try it
```bash
node -e 'function c(){let n=0;return ()=>++n} const a=c(); console.log(a(),a())'
node -e 'console.log([1,2,3,4].filter(x=>x%2===0).map(x=>x*10))'
node -e 'const o={n:"orl",hi(){return this.n}}; console.log(o.hi())'
```

## Optional scratch drills (inside a related lab's work directory)
1. `closure.mjs`: `makeAdder(n)` returns `(x) => x+n`; prove two adders hold independent `n`. Then `makeCounter()` with `inc()/get()` sharing one private `n`.
2. `hof.mjs`: given `[{n:'a',s:10},{n:'b',s:30},{n:'c',s:20}]`, `filter s>=20`, `map` names, `reduce` total score. No `for` loops.
3. `ship.mjs` — **hoist demo CLI**: declaration-callable-before-def vs `const`-arrow-TDZ (catch + print error). Plus `var`-in-loop bug vs `let` fix with pushed callbacks. Exit `0` with all three proofs printed.

## Break it
Use the explicit loop example: change `for (let i = 0; i < 3; i++)` to var and compare the stored callbacks' results. Changing a counter function's local let to var alone does not create the loop-binding bug. Revert and explain per-iteration bindings; log the actual reproducer in [[90-js-protips]].

## Check
1. Which function form can be called before its line (`function name(){}`), and which throws because it is used before its line (TDZ)?
2. What does a closure keep — a copy of the value, or access to the variable itself (so later changes are seen)?
3. Why do arrows make bad object methods (no own `this`) but great callbacks (short + use outer `this`)?
Gate: pass the relevant lab, explain independent closure instances, and demonstrate a failing test when state accidentally becomes shared. A ban on for loops or a syntax-only check does not assess functional reasoning.

## Related

- [[02-js-control-flow|Control Flow]]
- [[04-js-objects-prototypes|Objects & Prototypes]] (`this` full rules)
- [[05-js-arrays-iterables|Arrays & Iterables]]

Sources: [MDN functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions), [closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures), [arrow functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions). Lab verification: [[implementation-status]].
