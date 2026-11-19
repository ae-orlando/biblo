# Reference: serialization around an invariant

The function validates inputs, locks both accounts in ascending ID order, checks that both exist, and conditionally debits before crediting. A raised exception or overflow aborts the statement, preserving the pre-call state.

Consistent ordering reduces deadlocks for this function's pairwise locks; it does not prove a whole application cannot deadlock. Applications still need transaction boundaries, retry policy for appropriate SQLSTATEs, timeouts and idempotency for business operations.

Verification: `python3 90-tools/practice.py check pg-transfer --reference`.
