---
created: 2026-09-30
updated: 2026-10-21
---

# Transactions

> Outcome: state an invariant and prove all-or-nothing changes under failure. Prerequisite: [[07-updating-and-deleting-data]]. Practice: `pg-migration`, then `pg-transfer`, in [[practice-catalog]]. Continue into [[16-concurrency-and-application-sql]] for the concurrency/driver boundary.

## Why (Backend / Admin)

Multi-table writes must be atomic: owner + dog + tricks either all succeed or all roll back. Without a transaction, a crash mid-way leaves orphans.

ACID: **A**tomicity, **C**onsistency, **I**solation, **D**urability.

## Basics

```sql
BEGIN;
  INSERT INTO owners (name) VALUES ('Dana') RETURNING id;
  -- use returned id, e.g. 10:
  INSERT INTO dogs (name, age, owner_id) VALUES ('Rex', 2, 10);
COMMIT;
-- on error:
ROLLBACK;
```

- `psql` is autocommit: each statement commits unless wrapped in `BEGIN...COMMIT`.
- App drivers (`psycopg`, `node-postgres`, `SQLAlchemy`, Prisma `$transaction`): use their transaction helper — never string-concat `BEGIN` manually in app code if the driver pools connections.

## SAVEPOINT (Partial Rollback)

```sql
BEGIN;
  INSERT INTO owners (name) VALUES ('Eli');
  SAVEPOINT sp1;
  INSERT INTO dogs (name, age, owner_id) VALUES ('Bad', -5); -- CHECK fails
  ROLLBACK TO SAVEPOINT sp1;
COMMIT; -- keeps Eli, drops Bad
```

## Isolation (What You Need to Know)

Default `READ COMMITTED`: each statement sees committed data. Enough for most apps.

- Two concurrent `UPDATE`s to the same row: second waits, then proceeds (row lock).
- Lost-update / check-then-insert races (e.g. two signups creating same `UNIQUE` name): rely on `UNIQUE` + `ON CONFLICT`, not app-level `SELECT`-then-`INSERT`.
- For a multi-statement read/decision/write, lock relevant rows inside the transaction or use an appropriate higher isolation strategy. A single conditional atomic UPDATE can often implement a one-row invariant without a preceding SELECT. For multirow invariants, plan consistent lock ordering:

```sql
-- dogs.age as a stand-in counter; in real code this is accounts.balance / stock.qty
BEGIN;
  SELECT age FROM dogs WHERE id = 1 FOR UPDATE;
  UPDATE dogs SET age = age + 1 WHERE id = 1;
COMMIT;
```

Keep transactions short: open late, commit early. Long idle transactions block `VACUUM` and bloat tables (see [[13-admin-and-ops|Admin & Ops]]).

## Choosing Quickly

| Use this | When |
|---|---|
| `BEGIN...COMMIT` | 2+ writes that must succeed together |
| `ROLLBACK` | any error, discard all |
| `SAVEPOINT` | try risky step inside bigger txn |
| `SELECT ... FOR UPDATE` | read-modify-write on same row |
| Driver transaction helper | all app code (pool-safe) |

## Related Notes

- [[07-updating-and-deleting-data|Updating and Deleting Data]]
- [[13-admin-and-ops|Admin & Ops]]
- [[09-altering-tables|Altering Tables]]

## Practice and retrieval

In `pg-transfer`, make every invalid input leave balances unchanged, then run concurrent opposing calls. Explain why transactions do not automatically prevent all race conditions, why sequences can advance after a rollback, and why external side effects such as an email are not rolled back by SQL. Add an idempotency-key design before claiming retry-safe business transfers.

Sources: [Transactions tutorial](https://www.postgresql.org/docs/18/tutorial-transactions.html), [transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html).
