# Python lab: accumulate without changing input

**ID:** py-loops. Prerequisites: [[03-python-control-flow]], basic functions/string strip. Inputs are valid lists of the declared element types; broader shape validation comes later.

Implement:
- count_nonblank(lines): count strings whose strip() result is nonempty. Keep the original strings/list unchanged. Empty input → 0.
- sum_even(numbers): sum integer elements divisible by two, including negative values and zero. Empty/no-matching input → 0. Do not modify the list or retain totals between calls.

For [3,-4,0,8,5,2], the even sum is 6. For [' a ', '', ' \t', 'b\n', '\n', '0'], the nonblank count is 3.

```bash
python3 90-tools/practice.py start py-loops
python3 90-tools/practice.py check py-loops
```

Completion: explain accumulator initialization, each iteration and return placement. Deliberately return inside the first iteration and show the lost work. Extension: return both matching count and total under a newly documented contract; write your own checks first.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/py-loops/explanation.md)
