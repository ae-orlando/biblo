---
created: 2026-10-08
updated: 2026-10-21
---

# 04 — Objects & Prototypes (`this`, classes)

> Prerequisite: [[03-js-functions-scope]]. Practice: `js-data` in [[practice-catalog]]. Its frozen-input and arbitrary-key cases expose identity/mutation assumptions. Prototype/this demonstrations are additional self-authored scratch drills.

## Outcomes

After this note you can: tell what `this` will be from how a function is called; fix a detached-method crash with `bind` or an arrow wrapper; copy objects safely (know when to use spread vs full deep copy); write a class with private fields (`#pw`) and getters.

## Mental model
What an object is: a collection of named values. Example: `{ name: 'orl', age: 3 }` stores `name` and `age`. You read with `obj.name` or `obj['name']`.
What `this` is: inside a method (a function stored in an object), `this` means "the object before the dot". `o.hi()` → inside `hi`, `this` is `o`. If you copy the method out (`const f = o.hi`) and call `f()`, there is no object before the dot, so `this` is `undefined` — that is the detached-method bug.
What a prototype is: every object has a hidden link to another object (its prototype). If a property is missing on the object, JS looks at the prototype, then its prototype, and so on. A class is shorthand that sets up this link for you.

```js
const o = { a: 1, hi() { return this.a; } };
console.log(o.hi()); // 1 — this=o
const f = o.hi; // detached
// console.log(f()); // TypeError in strict/module (this=undefined)
console.log(f.call({ a: 9 })); // 9 — explicit this
```

## Literals, computed keys, shorthand
What they do: an object literal `{ ... }` creates an object. Shorthand `{ id }` means `{ id: id }`. Computed `[expr]` uses the result as the key name. `Object.keys()` lists own key names, `'k' in obj` also checks prototypes, `Object.hasOwn()` checks only the object itself.

```js
const k = 'id', id = 7;
const user = { id, [k + '2']: 8, 'with space': true, greet() { return this.id; } };
console.log(user.id, user.id2, user['with space']); // 7 8 true
console.log(Object.keys(user), 'greet' in user); // keys array, in checks proto chain too
console.log(Object.hasOwn(user, 'id')); // true — own only (modern; avoid hasOwnProperty)
console.log(Object.entries(user).length); // entries/keys/values for iteration
console.log(Object.fromEntries([['a', 1], ['b', 2]])); // {a:1,b:2} — inverse
```

## `this` — four rules (memorize order)
What decides `this`: how the function is called, not where it is written. 1) `obj.m()` → `this` is `obj`. 2) `.call/.apply/.bind` → `this` is the object you pass. 3) `new F()` → `this` is the fresh object being built. 4) plain `f()` → `this` is `undefined` in modules (never rely on it). Arrows ignore all four and use the surrounding `this`.

```js
const base = { n: 'base', who() { return this.n; } };
// 1. method call: obj.m() → this=obj
console.log(base.who()); // base
// 2. explicit: call/apply/bind
console.log(base.who.call({ n: 'x' })); // x
const bound = base.who.bind({ n: 'b' });
console.log(bound()); // b
// 3. new: this = fresh object inheriting prototype
function P(n) { this.n = n; }
console.log(new P('p').n); // p
// 4. default: undefined in modules/strict, globalThis in sloppy — never rely on it
// Arrow: no own this — inherits where written
const timer = { n: 't', start() { setTimeout(() => console.log(this.n), 0); } };
timer.start(); // t — arrow inside method sees timer
```

## Prototypes (what classes desugar to)
What it does: `Object.create(proto)` makes a new object whose hidden prototype link points at `proto`. Method calls missing on the new object are found on the prototype. `Object.getPrototypeOf()` reads that link.

```js
const animal = { speak() { return `${this.name}!`; } };
const dog = Object.create(animal); // dog.__proto__ = animal
dog.name = 'rex';
console.log(dog.speak(), Object.getPrototypeOf(dog) === animal); // rex! true
console.log(Object.hasOwn(dog, 'speak')); // false — inherited
```

## Classes
What they are: shorthand for creating objects with a shared prototype. `constructor()` runs when you call `new User(...)` and sets up the instance with `this.name = ...`. Methods like `greet()` live on the prototype (shared), not on each instance. `#pw` is a private field — only code inside the class can read it. `static` means "on the class itself, not on instances". `get` defines a property you read without `()`.

The password-named field below is a toy access-control example, **not secure credential storage**. Private fields do not hash passwords or make memory inaccessible to all debugging/runtime code. Real authentication belongs to a reviewed framework and password-hashing policy, not this class.

```js
class User {
  #pw; // private field — invisible outside
  static count = 0; // on class, not instances
  constructor(name, pw) { this.name = name; this.#pw = pw; User.count++; }
  greet() { return `hi ${this.name}`; } // on prototype
  static make(...a) { return new User(...a); } // factory
  get masked() { return '*'.repeat(String(this.#pw).length); } // getter, no ()
  set password(v) { if (v.length < 4) throw new Error('too short'); this.#pw = v; }
}
const u = new User('orl', 's3cr3t');
console.log(u.greet(), u.masked, User.count); // hi orl ****** 1
// console.log(u.#pw); // SyntaxError — private
console.log(u instanceof User, typeof User); // true function
```

WeakMap/WeakSet support weakly held objects (and eligible non-registered symbols in current ECMAScript), with a smaller API than Map/Set: no iteration or size. Collection timing is not observable as a reliable schedule. They are not interchangeable with enumerable data stores.

## Copy/merge (shallow!)
Spread copies enumerable own properties at the top level; nested references are still shared. structuredClone deeply clones supported structured-clone values, but cannot clone everything (functions throw; arbitrary prototypes/accessors are not preserved as class behavior). Object.freeze is shallow.

```js
const a = { x: 1, nest: { y: 2 } };
const b = { ...a, x: 99 }; // spread — top-level copy
b.nest.y = 999;
console.log(a.nest.y); // 999 — nested still shared!
console.log(structuredClone(a)); // deep clone (modern browsers + Node 17+)
console.log(JSON.parse(JSON.stringify(a))); // deep-ish, loses fns/undefined/BigInt
console.log(Object.freeze({ z: 1 })); // shallow freeze — nested still mutable
```

## Pitfalls
- A detached method does not retain its original receiver. A plain strict call gets undefined; timer callback receivers depend on the host (Node uses a Timeout receiver). The result can be wrong or throw. Use bind or a wrapper when a specific receiver is required.
- Arrow as method uses the surrounding `this`, not the object — write methods as `m() {}`.
- `==` / `===` on objects compare identity (same object in memory?), never contents — `{a:1} !== {a:1}` because they are two objects.
- Spread / `Object.assign` copy only the top level — changing a nested object leaks into the original; use `structuredClone` for a full copy.
- Top-level `this` is `undefined` in `.mjs` modules — write code that works with `undefined`, never assuming a global object.

## Try it
```bash
node -e 'const o={a:1,hi(){return this.a}}; const f=o.hi; console.log(o.hi(), f.call({a:9}))'
node -e 'class U{constructor(n){this.n=n} hi(){return this.n}} console.log(new U("x").hi())'
node -e 'const a={x:1,n:{y:2}}; const b={...a}; b.n.y=9; console.log(a.n.y)'
node -e 'console.log(Object.entries({a:1}), Object.fromEntries([["b",2]]))'
```

## Optional scratch drills (inside js-data/work)
1. `this.mjs`: object with method + arrow-method + detached-call + `call/bind` demos. Log which `this` each sees; fix detached with `bind`.
2. `proto.mjs`: `Object.create` chain `animal -> dog`, prove `speak` inherited not own, `getPrototypeOf` check. Then same via `class Dog extends Animal`.
3. `ship.mjs` — **clone + private class**: spread-copy with nested object, mutate nested, show leak. Fix with `structuredClone`, print both. Add `#private` class with getter/setter proving invisibility + validation throw.

## Break it
Call `const greet = u.greet; greet()` inside a try/catch in an ESM scratch file; compare with a timer callback in your actual host. Record the observed receiver/wrong value rather than assuming every host throws the same TypeError. Fix with a wrapper or bind and explain why.

## Check
1. What decides `this` — where the function is written, or how it is called? Which function kind ignores that rule (arrows)?
2. Spread copy: which level is safe (top level), which still shares (nested objects)?
3. Where do class methods live — on each instance, or shared on the prototype?
Gate: `proto.mjs` prints `false true` for own-vs-proto checks.

## Related

- [[03-js-functions-scope|Functions & Scope]]
- [[05-js-arrays-iterables|Arrays & Iterables]]

Sources: [MDN this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this), [classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes), [structuredClone](https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone). Lab verification: [[implementation-status]].
