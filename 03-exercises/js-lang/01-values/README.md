# Lab: parse a count without accidental coercion

**ID:** `js-values` · Node 24 recommended · Outcome: turn a precise input contract into validation and tests.

Prerequisites: [[01-js-values-types]], [[02-js-control-flow]], [[03-js-functions-scope]], [[12-js-errors-regex]], [[14-js-strings-numbers-dates]]. Read only the relevant function, string and error basics first; this is not a zero-prerequisite first line of code.

## Contract

Export `parseCount(input)` from `work/main.mjs`. Only string inputs are permitted; other types throw `TypeError`. Trim outer whitespace, require one or more ASCII decimal digits and return a safe nonnegative integer. Invalid syntax or range throws `RangeError`.

Examples: `' 42 '` → `42`, `'007'` → `7`, `'0'` → `0`. Reject `''`, `'42px'`, `'-1'`, `'+1'`, `'1e3'`, `'0x10'`, and numbers above `Number.MAX_SAFE_INTEGER`. Do not accept an object merely because it converts to a numeric string.

```bash
python3 90-tools/practice.py start js-values
python3 90-tools/practice.py check js-values
```

The checker imports your exported function. Logging correct answers without implementing the contract is insufficient.

## Completion and transfer

Explain why `Number('')`, `parseInt('42px')` and a truthiness test are inappropriate validators. Introduce one permissive-parser bug and show a failing case. Extend to a bounded page-size parser with a documented maximum and missing-value policy.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/js-values/explanation.md) · [Number.isSafeInteger](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isSafeInteger)
