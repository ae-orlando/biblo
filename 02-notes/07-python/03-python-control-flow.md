# Python 03 — decisions, loops and boundary cases

## Outcome

After [[02-python-values]], turn a decision table into branches and accumulate over a sequence without mutating it. Practice: py-decisions and py-loops.

An if condition selects a path. elif tests another condition only when previous branches were not taken; else is the remaining case. Indentation defines the suite. Comparison results are booleans; conditions also accept other values using truthiness.

```python
temperature = 18
if temperature < 10:
    description = "cold"
elif temperature < 25:
    description = "mild"
else:
    description = "hot"
print(description)  # mild
```

Test just below, exactly at and just above each threshold. Distinguish a valid zero from invalid input; if not amount rejects both zero and some missing values. Order overlapping branches intentionally. and/or short-circuit and return operands, not necessarily literal booleans.

## Iteration, not repeated hand-editing

```python
names = ["Ana", "Ben"]
for name in names:
    print(name)

total = 0
for number in [1, 2, 3]:
    total += number
print(total)  # 6
```

for visits values from an iterable; a list is an ordered sequence. range(3) supplies 0, 1, 2: the stop is excluded. Use enumerate when you need an index and value together. while repeats while its condition is true; ensure the state can change toward termination. break exits a loop; continue skips to its next iteration.

Initialize accumulators once before the loop and return after the loop when you need the full result. Returning inside the first iteration processes only the first value. Empty sequences should have an explicit meaningful result. Avoid removing elements from a list while iterating over that same list unless the algorithm deliberately handles that mutation.

## Practice and debugging

Use py-decisions to distinguish a shipping fee of zero from None (invalid input). Draw the score interval table before implementing grade. Use py-loops for blanks, negative even numbers and empty lists. Introduce an early return or wrong >= boundary, predict the failing test and repair it.

Transfer: add a new zone/threshold or a new counting predicate without changing unrelated cases. Explain why explicit loops are appropriate; a clever comprehension is not automatically clearer.

Next: [[04-python-functions]]. Source: [control flow](https://docs.python.org/3.14/tutorial/controlflow.html).
