# Python lab: decisions and exact boundaries

**ID:** py-decisions. Prerequisites: values, basic functions and [[03-python-control-flow]].

Implement two functions in work/main.py:
- shipping_fee(subtotal_cents, zone): local costs 500 below 5000 and zero from 5000; domestic costs 1200 below 10000 and zero from 10000. Negative/non-integer subtotals, booleans or other zones return None.
- grade(score): an integer 0..100 maps to A from 90, B from 80, C from 70, D from 60, otherwise F. Outside range/non-integer/boolean returns None.

None means invalid input; a shipping fee of 0 is a valid result. This lab deliberately uses a sentinel before the later exception contract.

```bash
python3 90-tools/practice.py start py-decisions
python3 90-tools/practice.py check py-decisions
```

Write the interval/decision table first. Tests cover just-below and exact thresholds, zero and malformed types. Completion: catch a deliberately wrong > versus >= and explain why bool must not count as an integer here. Change request: add a new shipping zone without changing unrelated cases.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/py-decisions/explanation.md)
