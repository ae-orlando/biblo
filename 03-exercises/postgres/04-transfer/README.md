# Lab: atomic transfers under concurrent callers

**ID:** `pg-transfer` · Outcome: preserve balances and total money under failures and contention.

Prerequisites: [[10-transactions]], [[16-concurrency-and-application-sql]]. This lab introduces a small PL/pgSQL function; use the linked lesson and official function documentation before attempting it.

## Contract

`fixtures.sql` creates three accounts with integer minor-unit balances `10000`, `10000`, `0`. Define:

```sql
transfer(source_id bigint, target_id bigint, amount bigint) RETURNS void
```

Reject missing accounts, NULL/nonpositive amounts, identical source/target IDs and insufficient funds. Successful transfers subtract and add exactly once. Failed transfers change no balance. Lock both existing accounts in a consistent order before checking and updating.

```bash
python3 90-tools/practice.py start pg-transfer
python3 90-tools/practice.py check pg-transfer
```

The checker runs invalid cases and concurrent opposite-direction transfers. It does not rely on sleeps or a fixed speedup. It verifies balances, not merely that calls returned success.

## Completion and transfer

Explain why a read followed by a write outside a transaction loses updates. Describe where a pooled application must acquire and release its connection. Add an idempotency-key design to prevent retrying a completed business transfer twice; this function alone does **not** provide that feature.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/pg-transfer/explanation.md) · [Explicit locking](https://www.postgresql.org/docs/18/explicit-locking.html)
