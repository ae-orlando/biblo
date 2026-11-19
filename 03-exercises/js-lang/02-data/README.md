# Lab: aggregate orders without mutating input

**ID:** `js-data` · Outcome: implement a pure transformation with explicit data invariants.

Prerequisites: [[03-js-functions-scope]], [[04-js-objects-prototypes]], [[05-js-arrays-iterables]], [[12-js-errors-regex]].

## Contract

Export `summarizeOrders(orders)` from `work/main.mjs`. Input must be an array of records with nonblank string `id` and `user`, safe nonnegative integer `cents`, and status `paid` or `cancelled`. Reject malformed records and duplicate IDs, including duplicates on cancelled records. Preserve original user strings as grouping keys.

Sum only paid records. Return new `{user, count, cents}` records ordered by JavaScript string comparison of `user` (not locale-dependent collation). Do not return users having only cancelled records. Reject an unsafe total. Never mutate input or carry state across calls.

Example: Ben's paid orders `200` and `25` → `{user:'Ben',count:2,cents:225}`. An empty array produces `[]`. A user named `__proto__` is ordinary data.

```bash
python3 90-tools/practice.py start js-data
python3 90-tools/practice.py check js-data
```

## Completion and transfer

Explain why integer minor units still need range checks and why a Map is convenient for arbitrary keys. Add refunds with a separately defined sign/status policy. Write a regression test for repeated calls and frozen input.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/js-data/explanation.md) · [Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
