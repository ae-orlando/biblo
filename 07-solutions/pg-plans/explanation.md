# Reference: a workload-specific access path

The partial composite index stores only login events, groups them by user, and orders recent IDs within each user. It fits the stated predicate/order/limit. Another workload may need a different index or no extra index.

The test prints an actual JSON plan but does not grade your interpretation. Save your own before/after measurements and discuss selectivity, cache effects, statistics, heap fetches and write cost. Do not extrapolate this small fixture into a production speed guarantee.

Verification: `python3 90-tools/practice.py check pg-plans --reference`; manual interpretation remains separate.
