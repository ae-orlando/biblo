---
created: 2026-09-30
updated: 2026-10-21
---

# Admin & Ops

> Outcome: prove effective least privilege and recover into a separate database. Prerequisites: [[01-psql-workflow]], [[10-transactions]]. Practice: `pg-restore` in [[practice-catalog]]. Host service and backend-cancellation commands below are administration reference, not permission to alter an existing service/session.

Companion: [[01-psql-workflow|psql Workflow]] for per-project user/DB creation.

## Roles & Privileges (Least Privilege for Apps)

Never use `postgres` superuser in apps. One role per app, minimal grants:

Separate an owning/migration role from the runtime app role. Ownership and membership can bypass the intended grant restriction. The following snippets assume the owner/migrator creates objects and an administrator has deliberately created the named non-owner runtime roles.

```sql
-- Read-write app role
GRANT CONNECT ON DATABASE appdb TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user; -- for SERIAL ids

-- Future tables
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO app_user;

-- Read-only role (analytics / debug)
GRANT CONNECT ON DATABASE appdb TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
  GRANT SELECT ON TABLES TO readonly_user;

-- Revoke / inspect
REVOKE DELETE ON dogs FROM app_user;
SELECT grantee, privilege_type FROM information_schema.role_table_grants WHERE table_name='dogs';
```

In `psql`: `\du` (roles), `\dp dogs` / `\z dogs` (table ACLs).

Default privileges apply to future objects created by app_owner, not all creators. Test effective access with SET ROLE and negative operations. Do not grant ownership to a role you expect to be read-only.

## Service (Arch) & Connections

```bash
sudo systemctl enable --now postgresql.service
sudo systemctl status postgresql.service
journalctl -u postgresql.service -f  # logs

# Connection string (.env)
# postgres://<user>:<password>@localhost:5432/<db>
psql -U app_user -d appdb -h localhost
```

Stuck / idle transactions blocking deploys:

```sql
SELECT pid, usename, state, query, now() - query_start AS duration
FROM pg_stat_activity WHERE datname = 'appdb';

-- Kill one (prefer pg_cancel_backend first, terminate if stuck)
SELECT pg_cancel_backend(pid);
SELECT pg_terminate_backend(pid);
```

Store password out of history: `~/.pgpass` (`chmod 600`), format `host:port:db:user:password`.

## Backup & Restore

```bash
# Full backup (custom format, best for restore)
pg_dump -U app_user -h localhost -Fc appdb -f appdb_$(date +%F).dump

# Plain SQL (grep-able, slower restore)
pg_dump -U app_user -h localhost appdb -f appdb.sql

# Restore into a deliberately created, empty scratch database, NOT the original
pg_restore -U restore_owner -h localhost -d appdb_restore appdb_2026-09-30.dump
psql -X -v ON_ERROR_STOP=1 -U restore_owner -h localhost -d appdb_restore -f appdb.sql

# Schema only / data only / one table
pg_dump -U app_user -h localhost --schema-only appdb -f schema.sql
pg_dump -U app_user -h localhost --data-only -t dogs appdb -f dogs.sql
```

- Test restores on a scratch DB — untested backups don't count.
- A least-privilege runtime app role may be unable to recreate schema/ownership. Plan a separate restore identity. Database dumps do not by themselves recreate all cluster-wide roles, external services or application secrets.
- Pre-migration: `pg_dump -Fc` + verify size/timestamp before `ALTER` (see [[09-altering-tables|Altering Tables]]).

## Size & Health

```sql
-- Sizes
SELECT pg_size_pretty(pg_database_size('appdb'));
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;

-- Bloat / stats (autovacuum usually handles this; manual after bulk ops)
VACUUM (ANALYZE, VERBOSE) dogs;
ANALYZE dogs; -- refresh planner stats after bulk load, see [[11-indexes-and-performance|Indexes & Performance]]

-- Long-running / locks
SELECT * FROM pg_stat_activity WHERE state != 'idle';
```

Rule: rely on autovacuum; run manual `VACUUM ANALYZE` after bulk `INSERT/UPDATE/DELETE`, never `VACUUM FULL` on prod without downtime window (rewrites + exclusive lock).

## Related Notes

- [[01-psql-workflow|psql Workflow]]
- [[09-altering-tables|Altering Tables]]
- [[11-indexes-and-performance|Indexes & Performance]]

## Practice and retrieval

Complete `pg-restore`: prove SELECT succeeds and DML/DDL fails, verify future-table access, restore elsewhere, then test data, constraints and sequence behavior. Explain recovery point/time objectives, retention and offsite/encryption requirements without enabling a remote service automatically. Do not destroy the source merely to test recovery.

Sources: [Privileges](https://www.postgresql.org/docs/18/ddl-priv.html), [default privileges](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html), [backup](https://www.postgresql.org/docs/18/backup.html).
