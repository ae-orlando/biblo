# Reference: validation and aggregation boundaries

The reference validates required fields, detects duplicate IDs, normalizes category keys and builds local aggregate records. It sorts output keys explicitly and does not return caller-owned records as internal state. Boolean cents are rejected even though bool subclasses int.

Verification: `python3 90-tools/practice.py check py-records --reference`. Transfer requires a changed policy, not just reproducing the same dictionary loop.
