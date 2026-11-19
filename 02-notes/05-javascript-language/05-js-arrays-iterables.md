---
created: 2026-10-08
updated: 2026-10-21
---

# 05 — Arrays & Iterables (`map`, `Set`, `Map`)

> Prerequisites: [[03-js-functions-scope]], [[04-js-objects-prototypes]]. Practice: `js-data`, then `js-async`, in [[practice-catalog]]. Copying an array is shallow; its objects can still be shared. Mutation can be appropriate inside a well-defined local boundary.

## Outcomes

After this note you can: transform lists with `map`/`filter`/`reduce` instead of loops; tell which methods change the original array (`sort`, `splice`) vs return a new one (`map`, `toSorted`); remove duplicates with `Set` and look up by id with `Map`; read the last item with `at(-1)` and combine sets with `union`/`intersection`/`difference`.

## Mental model
What an array is: an ordered list like `[3, 1, 2]`. Array methods transform lists without you writing `for` by hand. The key split: mutating methods change the original array (`sort`, `splice`), copying methods return a new array and leave the original alone (`map`, `filter`, `toSorted`). In UI code always prefer the copying ones.
What iterable means: anything you can loop with `for...of` or expand with `...`. This includes arrays, strings, `Map`, `Set`.
What `Map` / `Set` are: `Map` is a dictionary where keys can be anything (objects too, unlike plain `{}`). `Set` is a collection that keeps only unique values. Both remember insertion order.

```js
const xs = [3, 1, 2];
console.log(xs.map((x) => x * 2));       // [6,2,4] — new array
console.log(xs.filter((x) => x > 1));    // [3,2]
console.log(xs.toSorted((a, b) => a - b), xs); // [1,2,3] [3,1,2] — toSorted copies; sort() mutates!
console.log(xs.slice(0, 2));             // [3,1] — non-mutating; splice() mutates
console.log(xs.at(-1));                  // 2 — at() allows negative index (ES2022)
```

## The 10 you use daily
What they do: `find` returns the first matching item (or `undefined`). `findLast` returns the last match. `some` asks "does any item pass?", `every` asks "do all pass?". `reduce` boils the array to one value (sum, total). `flat` unwraps nested arrays. `Object.groupBy` sorts items into buckets by key.

```js
const users = [{ n: 'a', s: 10 }, { n: 'b', s: 30 }, { n: 'c', s: 20 }];
console.log(users.find((u) => u.s > 15)?.n); // b — first match (?.
console.log(users.findLast((u) => u.s > 15)?.n); // c — last match (ES2023)
console.log(users.some((u) => u.s > 25), users.every((u) => u.s > 5)); // true true
console.log(users.reduce((t, u) => t + u.s, 0)); // 60
console.log(users.toSorted((a, b) => b.s - a.s).map((u) => u.n)); // ['b','c','a']
console.log([1, [2, [3]]].flat(2)); // [1,2,3]
console.log(Object.groupBy(users, (u) => (u.s >= 20 ? 'hi' : 'lo'))); // ES2024 — {hi:[...], lo:[...]}
```

`find` + `?.` kills `if (x) x.y` pyramids. `reduce` replaces accumulator loops.

## Mutation map (which methods change the array?)
What it means: mutating methods rewrite the array in place. Copying methods leave it alone and return a new array. Rule: in UI state, always use the copying family so you don't accidentally change displayed data.

Mutating: `push/pop/shift/unshift/splice/sort/reverse/fill/copyWithin`. Copying: `map/filter/slice/concat/flat/toSorted/toReversed/toSpliced/with`. Rule: in UI state, always use the copying family.

```js
const a = [1, 2, 3];
console.log(a.with(1, 99), a); // [1,99,3] [1,2,3] — with() copies (ES2023)
```

## `Map` / `Set` (+ full ES2025 algebra)
What they do: `m.set(k, v)` stores, `m.get(k)` reads, `m.size` counts. `new Set(arr)` drops duplicates. Set algebra: `union` keeps items in either set, `intersection` keeps items in both, `difference` keeps items only in the first.

```js
const m = new Map([['a', 1]]);
m.set({ k: 1 }, 'obj-key'); // any value as key — impossible with {}
console.log(m.get('a'), m.size); // 1 2
for (const [k, v] of m) console.log(k, '=>', v);
const s = new Set([1, 1, 2, 3]);
console.log([...s], s.has(2)); // [1,2,3] true — dedupe idiom
// ES2025 Set algebra (Node 22+):
const A = new Set([1, 2]), B = new Set([2, 3]);
console.log(A.union(B));        // {1,2,3}
console.log(A.intersection(B)); // {2}
console.log(A.difference(B));   // {1}
```

## Iterables + generators + destructuring
What they do: spreading a string (`[...'hi']`) splits it into characters. A generator (`function*`) produces values lazily with `yield`, one at a time. `[first, ...rest] = arr` pulls the first item into `first` and the remainder into `rest`.

```js
const str = 'hi';
console.log([...str], [...'😀'].length); // ['h','i'] 1 — spread respects code points
function* gen() { yield 1; yield 2; }
console.log([...gen()], [...Array(3).keys()]); // [1,2] [0,1,2]
const [first, ...rest] = [10, 20, 30];
console.log(first, rest); // 10 [20,30]
```

## Pitfalls
- `[10,9].sort()` without a compare function sorts as text (`[10,9]` stays) — always pass `(a,b) => a-b` for numbers.
- `sort` / `splice` / `reverse` rewrite the original array — in UI state use `toSorted` / `toSpliced` / `toReversed` which return new arrays.
- `Array(3)` makes empty holes that `.map` skips — build with `Array.from({length:3}, (_,i)=>i)`.
- `for...in` on arrays, `==` on arrays, and `typeof []` (says `'object'`) all mislead — check arrays with `Array.isArray` and loop with `for...of`.
- `flat` / `groupBy` / `with` need modern runtimes — fine on Node v24 here, check compat for old browsers.

## Try it
```bash
node -e 'console.log([3,1,2].toSorted((a,b)=>a-b)); console.log([...new Set([1,1,2])])'
node -e 'console.log([{s:1},{s:9}].reduce((t,u)=>t+u.s,0))'
node -e 'console.log(new Set([1,2]).union(new Set([2,3])), new Set([1,2]).intersection(new Set([2,3])), new Set([1,2]).difference(new Set([2,3])))'
node -e 'console.log([10,20,30].at(-1))'
```

## Optional scratch drills (inside js-data/work)
1. `stats.mjs`: validate argv numbers and compute sum/avg/min/max. Reject empty input explicitly: ?? does not detect NaN or the infinities produced by min/max on no values. Choose a readable loop or reduction and test both boundaries and ordinary data.
2. `dedupe.mjs`: `[...new Set(arr)]` + `Map`-by-`id` keeping last occurrence of `[{id,...}]`. Show `sort` bug (`[10,9].sort()`) then comparator fix, plus `toSorted` non-mutation proof.
3. `ship.mjs` — **group dashboard**: `Object.groupBy` users by `hi/lo`, then `map` names + `reduce` totals per group. Iterate a `Map` with `for...of` + destructured `[k,v]`. Print `at(-1)` last-user and one `intersection` demo.

## Break it
In `dedupe.mjs`, replace `toSorted` with `sort` and print the source array before/after — observe the mutation. Revert, re-run to prove the original is untouched. Log `sort-mutates → UI-state bug → toSorted` in [[90-js-protips]].

## Check
1. Which methods rewrite the original array, and what do you use instead in UI state (copying versions)?
2. Remove duplicates from an array in one expression with `Set` — what is it?
3. `union` / `intersection` / `difference`: what does each keep (either, both, only-first)?
Gate: `stats.mjs` with no args exits `1` with usage on `stderr`.

## Related

- [[03-js-functions-scope|Functions & Scope]]
- [[06-js-destructuring-modules|Destructuring & Modules]]

Sources: [MDN Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array), [Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map), [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set). Check runtime compatibility for newer convenience methods. Lab verification: [[implementation-status]].
