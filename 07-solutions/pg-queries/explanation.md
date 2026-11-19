# Reference: missing rows and deterministic latest events

The left join retains users; `count(l.id)` ignores the generated NULL placeholder. `NOT EXISTS` tests whether a correlated set contains a row without introducing `NOT IN`'s NULL ambiguity. `row_number` needs an explicit tie-breaker to select a deterministic latest event.

A CTE, subquery or `DISTINCT ON` can also express parts of this task. Defend the choice using clarity and measured plans, not a universal claim that joins outperform subqueries. Remove the ID tie-breaker and demonstrate why the contract is no longer guaranteed.

Verification: `python3 90-tools/practice.py check pg-queries --reference`.
