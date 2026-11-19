---
created: 2026-09-30
updated: 2026-10-21
---

# Altering Tables

> Outcome: evolve existing data and constraints atomically, then reason about deployment compatibility and locks. Prerequisites: [[07-updating-and-deleting-data]], [[10-transactions]]. Practice: `pg-migration` in [[practice-catalog]]. Commands below are alternatives, not one sequential script.

For initial `CREATE TABLE`, see [[02-sql-datatypes|SQL Datatypes]] and [[03-inserting-and-viewing-data|Inserting and Viewing Data]].

## ADD / DROP / RENAME Column

```sql
ALTER TABLE dogs ADD COLUMN breed TEXT;
ALTER TABLE dogs ADD COLUMN IF NOT EXISTS breed TEXT DEFAULT 'mix' NOT NULL;

ALTER TABLE dogs DROP COLUMN breed;
ALTER TABLE dogs DROP COLUMN IF EXISTS breed;

ALTER TABLE dogs RENAME COLUMN name TO dog_name;
ALTER TABLE dogs RENAME TO canines; -- rename table
```

- `ADD COLUMN ... NOT NULL` without `DEFAULT` fails on non-empty tables — add as nullable, backfill, then `SET NOT NULL`.
- Use versioned, reviewed migrations with explicit preconditions. IF EXISTS/IF NOT EXISTS can be useful in a deliberate script, but can also conceal schema drift; they are not a general migration-safety guarantee.

## Change Type / Default / Constraint

```sql
-- Widen VARCHAR (safe)
ALTER TABLE dogs ALTER COLUMN name TYPE VARCHAR(100);

-- Narrow or change type (may need USING)
ALTER TABLE dogs ALTER COLUMN age TYPE SMALLINT USING age::SMALLINT;

ALTER TABLE dogs ALTER COLUMN age SET DEFAULT 0;
ALTER TABLE dogs ALTER COLUMN age DROP DEFAULT;

ALTER TABLE dogs ALTER COLUMN name SET NOT NULL;
ALTER TABLE dogs ALTER COLUMN name DROP NOT NULL;
```

- A type change may rewrite a table/index or may be metadata-only depending on the conversion. ALTER operations still require locks. For large/active tables, plan expand/backfill/validate/contract with compatible application versions rather than assuming a cast is safe.

## ADD / DROP Constraints

```sql
ALTER TABLE dogs ADD CONSTRAINT age_nonneg CHECK (age >= 0);
ALTER TABLE dogs DROP CONSTRAINT age_nonneg;

ALTER TABLE owners ADD CONSTRAINT owners_name_unique UNIQUE (name);

-- Add FK after the fact
ALTER TABLE dogs ADD CONSTRAINT dogs_owner_fk
  FOREIGN KEY (owner_id) REFERENCES owners (id) ON DELETE SET NULL;
```

List constraints in `psql`: `\d dogs`.

For CHECK and FK constraints, NOT VALID can separate enforcement for new writes from validation of existing data. It is not available for every constraint type and does not remove all lock requirements:

```sql
ALTER TABLE dogs ADD CONSTRAINT age_nonneg CHECK (age >= 0) NOT VALID;
ALTER TABLE dogs VALIDATE CONSTRAINT age_nonneg;
```

## DROP TABLE

```sql
DROP TABLE IF EXISTS dogs; -- fails if something references it
DROP TABLE dogs CASCADE;   -- also drops dependent FKs/views (dangerous, preview first)
```

- `CASCADE` is destructive — run `\d` / check dependents before using in prod. In apps, migrations should almost never use `CASCADE` blindly.

## Backend Migration Pattern

1. Deploy 1: `ADD COLUMN ... NULL` (backward-compatible).
2. Backfill + dual-write in app code.
3. Deploy 2: `SET NOT NULL` / add `CHECK` with `NOT VALID` + `VALIDATE`.
4. Drop old column.

Plan compatibility across old and new application versions. A recorded migration need not be arbitrarily re-runnable; it must apply to its documented predecessor and detect unexpected state. Some data changes are not fully reversible—state the recovery plan honestly.

## Practice and retrieval

Complete `pg-migration` against valid and conflicting data. Explain why “it failed halfway” is unacceptable if earlier backfill writes committed. Propose a different plan for millions of active rows, including lock timeout, validation and rollback/recovery limits.

Sources: [ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html).

## Related Notes

- [[02-sql-datatypes|SQL Datatypes]]
- [[13-admin-and-ops|Admin & Ops]]
- [[10-transactions|Transactions]]
