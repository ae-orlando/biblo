# Reference: framing before formatting

The reference quotes the directory, selects immediate regular files and emits basenames using GNU find's NUL formatting. GNU sort's NUL mode preserves records; C locale defines deterministic byte order.

A read-only pipeline can still fail; `pipefail` preserves an earlier stage's failure. Mutation to catch: replacing NUL with newline or using `for f in $(ls ...)`. Verification: `python3 90-tools/practice.py check bash-quoting --reference`.
