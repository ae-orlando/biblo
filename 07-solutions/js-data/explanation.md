# Reference: pure aggregation with business rules

The reference validates every order, tracks every ID, then skips cancelled totals. A Map isolates arbitrary user keys from object prototypes. New aggregate records and a new output array avoid input mutation; local variables prevent state leaking across calls.

Loops are not a failure of functional programming. A clear loop can express validation and grouping more directly than a clever reduction. Mutation to catch: using `orders.sort()` or a plain inherited-key accumulator. Verification: `python3 90-tools/practice.py check js-data --reference`.
