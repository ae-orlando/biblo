# Reference: narrow permissions changes

The reference checks the marker and required path types before applying any mode changes. It never uses sudo, chown or recursive chmod and never changes file content. The tests verify modes, preservation, repeatability and a symlink refusal.

This private-sandbox exercise is not a race-resistant privileged filesystem utility. Parent traversal permissions, ACLs, mount flags and security modules can also affect real access. Verification: `python3 90-tools/practice.py check linux-permissions --reference`.
