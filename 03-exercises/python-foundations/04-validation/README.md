# Python lab: a precise count parser

**ID:** py-validation. Prerequisites: functions/strings and [[06-python-errors]].

Export parse_count(text). Reject non-string inputs with TypeError. Trim surrounding whitespace, then require one or more ASCII decimal digits representing 0..100000 inclusive; malformed syntax/out-of-range values raise ValueError.

' 42 ' → 42, '007' → 7 and '0' → 0. Reject blanks, signs, fractions, exponents, underscores, suffix junk and non-ASCII digit strings. Do not use eval. Raw int() accepts a broader vocabulary than this contract.

```bash
python3 90-tools/practice.py start py-validation
python3 90-tools/practice.py check py-validation
```

Completion: distinguish original type, complete syntax and numeric range checks. Show a regression catching a permissive conversion. Extend to a page-size parser with an explicit missing/default policy without treating zero or invalid input as missing automatically.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/py-validation/explanation.md)
