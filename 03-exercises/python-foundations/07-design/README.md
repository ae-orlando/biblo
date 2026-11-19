# Python lab: own state and preserve inventory invariants

**ID:** py-design. Prerequisites: collections/errors, [[09-python-objects]] and testing basics.

Implement Inventory with independent instance state:
- add(sku,quantity): nonempty already-trimmed unique string SKU; nonnegative integer quantity excluding bool; invalid/duplicate → ValueError.
- get(sku): return an immutable record exposing sku/available; absent → KeyError.
- reserve(sku,quantity): require a positive integer excluding bool and sufficient stock; otherwise ValueError (missing SKU → KeyError). Return the updated immutable record. Rejected operations change no state.
- snapshot(): fresh list of {'sku':..., 'available':...} dictionaries sorted by SKU. Mutating it must not change inventory.

```bash
python3 90-tools/practice.py start py-design
python3 90-tools/practice.py check py-design
```

Completion: explain class-versus-instance state, record mutability and why a public mutable internal dictionary bypasses invariants. Add a validated replenishment operation and negative tests. This single-process domain model is not a concurrency-safe database or security boundary.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/py-design/explanation.md)
