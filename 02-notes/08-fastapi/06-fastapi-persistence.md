# FastAPI 06 — persistence, transactions and migrations

## Outcome and prerequisites

After API contracts plus PostgreSQL modeling/transactions/concurrency, persist data through an explicit adapter and preserve invariants with concurrent requests. Practice: api-postgres. SQL is now relevant; it was not a prerequisite to beginning Python.

An in-memory dictionary disappears on restart and is not shared across worker processes. A lock in one Python object does not coordinate separate processes or other database clients. Put durable invariants in database constraints/transactions as well as request validation.

## Own a connection for an operation

The lab repository stores a DSN, not one global shared connection. Each synchronous operation acquires a connection and uses its context manager for commit/rollback/close. Values are passed through psycopg parameters, never formatted into SQL strings. Identifiers need their own trusted composition/allowlist policy; value placeholders cannot represent arbitrary table names.

Synchronous routes are intentional because this adapter uses blocking psycopg calls. A production pool needs capacity, acquisition timeout and transaction cleanup policies; “add a pool” is not automatic correctness or unlimited concurrency.

## Prevent overselling where the write happens

An application-level read followed by subtraction can race. A conditional atomic UPDATE can subtract only when enough stock remains and return the changed row. A CHECK constraint remains a final nonnegative invariant. Missing resource and insufficient stock are distinct outcomes; the lab supports reservations but not concurrent deletion of those rows.

Startup creates a tiny lab schema only in a disposable practice database. That bootstrap is **not** production migration management. Real changes need recorded predecessor versions, compatibility with old/new application code, lock/backfill planning, testing and recovery. A framework model does not erase these requirements.

## Practice and transfer

Complete api-postgres, reopen the app on the same database to demonstrate persistence, then run competing reservations and verify only available stock succeeds. Explain every commit/rollback boundary. Use the existing pg-migration/pg-restore labs to extend operational evidence.

Change request: prevent a client's retried successful reservation from reserving twice using a durable idempotency-key design. Do not confuse “atomic decrement” with “retry-safe business operation.” Document unresolved production roles, migration, pooling and backup decisions.

Sources: [psycopg transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html), [parameter passing](https://www.psycopg.org/psycopg3/docs/basic/params.html), [PostgreSQL concurrency](https://www.postgresql.org/docs/18/mvcc.html), [FastAPI SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/).
