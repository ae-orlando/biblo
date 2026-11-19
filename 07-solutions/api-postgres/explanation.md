# Reference: the invariant belongs at the write

The factory injects a repository/DSN, lifespan bootstraps only the lab schema and sync routes use a blocking psycopg adapter. Connections are owned per operation; parameters carry values. Conditional UPDATE plus CHECK prevents negative stock, while conflicts/missing resources map to deliberate HTTP errors.

The concurrency test sends ten reservations against three units and requires exactly three successes. No real application database is touched. Verification: `python3 90-tools/practice.py check api-postgres --reference`. Production needs migrations, least privilege, pooling/timeouts, idempotency and operational evidence beyond this fixture.
