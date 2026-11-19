# Python lab: validated sales aggregation

**ID:** py-records. Prerequisites: functions, collections and errors.

Implement summarize_sales(records). Require a list of dictionaries with a nonempty already-trimmed string id, nonblank string category and nonnegative integer cents excluding booleans. Reject duplicate exact IDs and malformed records with TypeError/ValueError. Other unrelated record fields are ignored.

Normalize categories with strip().lower(), aggregate count/cents and return new dictionaries ordered by Python string comparison of category. Never mutate the input or share accumulators across calls. Empty input → [].

Example: Travel amounts 90 and 10, with case/outer whitespace variants, produce {'category':'travel','count':2,'cents':100}; an office record with zero cents still counts.

```bash
python3 90-tools/practice.py start py-records
python3 90-tools/practice.py check py-records
```

Completion: explain dictionary/set roles and mutation boundaries, show a duplicate/state-leak defect caught by a test, then add a refund policy with its own valid/invalid cases. Do not infer real financial correctness from integer arithmetic alone.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/py-records/explanation.md)
