# Reference: evidence before intervention

The reference validates the PID, checks readability, then selects labeled fields from /proc status. The operation is read-only. It does not treat a successful read as a timeless guarantee that the same process still exists.

Use process groups and identity checks when a later operation must affect a specific process; PID reuse matters. Verification: `python3 90-tools/practice.py check linux-processes --reference`.
