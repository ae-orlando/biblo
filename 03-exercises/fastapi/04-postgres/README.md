# FastAPI lab: durable reservations that cannot oversell

**ID:** api-postgres. Prerequisites: factories/testing, PostgreSQL schema/transactions/concurrency and [[06-fastapi-persistence]]. Export create_app(dsn); the checker injects an explicit DSN for a disposable database in the private vault cluster. Never substitute a system/default/real database.

Create the tiny inventory schema during lab lifespan startup. POST /items accepts exactly sku (trimmed uppercase ASCII letters/digits with subsequent underscore/hyphen allowed, 1..40 characters) and strict integer available 0..1000000. Return 201 {id,sku,available}; duplicate → 409. GET /items/ID returns persisted state or 404.

POST /items/ID/reserve accepts exactly strict integer quantity 1..1000000. Atomically subtract only if stock suffices; return updated record/200, missing → 404, insufficient → 409. Invalid bodies → 422. Persistence must survive a new app instance and concurrent requests must not oversell. Use parameterized values and deliberate transaction/connection cleanup.

```bash
python3 90-tools/practice.py start api-postgres
python3 90-tools/practice.py check api-postgres
```

The checker starts only the marked vault cluster and creates/drops unique test databases. Completion: explain SQL invariants and every commit/rollback; add an idempotency-key design for retried reservations. Lab bootstrap DDL, admin connection and per-operation connections are not production migration/role/pooling policy.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/api-postgres/explanation.md)
