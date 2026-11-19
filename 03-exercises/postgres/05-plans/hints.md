# Plan lab — progressive hints

1. Equality on the leading column and a compatible order/limit can reduce the work needed for this particular query.
2. A partial index is eligible only when the planner can establish that the query implies its predicate. Parameterized predicates and generic plans need care.
3. Compare workload and selectivity, not “index good, sequential bad.” Costs are not milliseconds; actual node values must be interpreted with their loop counts.
