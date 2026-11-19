# Python lab: your first returned calculation

**ID:** py-basics. Read [[01-python-execution]] and [[02-python-values]] first. No previous Python/framework knowledge or package installation is required.

Implement total_cents(unit_price_cents, quantity) in work/main.py. Inputs for this first task are already valid nonnegative integers; return their integer total, not printed text, a float or one hard-coded example. Input validation is introduced in later labs.

Examples: 199 cents × 3 → 597; a zero price or zero quantity → 0. Python integers can exceed a typical 64-bit range; do not convert through float.

```bash
python3 90-tools/practice.py start py-basics
python3 90-tools/practice.py check py-basics
```

Edit the created work/main.py, not starter/ or 07-solutions/. The supplied NotImplementedError is an intentional temporary marker; replace it after understanding the lesson. The checker calls the function, so a definition-only file need not print anything.

Completion: explain definition versus call and return versus print. Predict a new price/quantity before checking it. Then write a separate scratch function converting a number of minutes to seconds without editing the supplied test answers.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/py-basics/explanation.md)
