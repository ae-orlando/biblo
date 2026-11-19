# Concurrency and application SQL boundaries

## Outcome and prerequisites

After [[10-transactions]], preserve an invariant under concurrent callers and explain how an application acquires the correct transaction connection. Practice: `pg-transfer` and `pg-restore`.

## Isolation is about observations, not just commands

Under READ COMMITTED, each statement gets a fresh snapshot of committed data. A row lock serializes conflicting writers, but does not make an earlier unlocked read current. Prefer a single conditional update for a one-row invariant, or lock the relevant rows before a multirow decision.

```sql
UPDATE accounts SET balance = balance - $1
WHERE id = $2 AND balance >= $1
RETURNING balance;
```

This is a parameterized application fragment. No returned row means the condition/account did not match; decide the error contract. Never build SQL by concatenating untrusted values. Parameters represent values, not arbitrary identifiers; use a trusted identifier-composition facility or allowlist for dynamic identifiers.

For two-row transfers, lock rows in the same order in every caller. Keep transactions short. READ COMMITTED does not prevent every anomaly; REPEATABLE READ/SERIALIZABLE change guarantees and may require retrying the **whole transaction** after serialization failures. A retry must not duplicate an external side effect or a completed business operation; idempotency is a separate requirement.

## Pooling and boundaries

Acquire one connection for a transaction, execute BEGIN/commands/COMMIT or the driver's transaction helper on that same connection, and roll back on failure before returning it. Helpers are preferable where documented; issuing BEGIN through unrelated pool.query calls is unsafe because calls can use different connections. Never leave failed/idle transactions checked out.

Distinguish schema owner/migrator from the runtime application role. Effective privileges include role membership, ownership and PUBLIC grants. Default privileges are tied to the role that creates future objects, not a universal per-schema policy.

## PL/pgSQL bridge for the transfer lab

The lab asks for a database-side function, not an application driver:

```sql
-- Illustrative fragments, not a complete function:
PERFORM id FROM accounts WHERE id IN (source_id,target_id) ORDER BY id FOR UPDATE;
GET DIAGNOSTICS locked_count = ROW_COUNT;
IF locked_count <> 2 THEN RAISE EXCEPTION 'account missing'; END IF;
```

`PERFORM` runs a query without returning its rows to the caller. `FOUND` and ROW_COUNT describe the relevant preceding statement; inspect them before another statement replaces the evidence. An uncaught exception aborts the statement. A function cannot independently commit the caller's transaction like an application transaction helper.

## Practice and retrieval

Complete `pg-transfer`; explain the concurrent schedule and unchanged balances after every rejected call. Design a transfer request ID stored with the operation to make repeated requests safe. Then use `pg-restore` to demonstrate effective permissions, not merely list grants.

Sources: [Isolation](https://www.postgresql.org/docs/18/transaction-iso.html), [locking](https://www.postgresql.org/docs/18/explicit-locking.html), [PL/pgSQL statements](https://www.postgresql.org/docs/18/plpgsql-statements.html), [default privileges](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html).
