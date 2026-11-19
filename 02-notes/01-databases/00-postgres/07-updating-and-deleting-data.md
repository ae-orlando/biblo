---
created: 2026-09-30
updated: 2026-10-21
---

# Updating and Deleting Data

> Outcome: preview affected rows, verify RETURNING results and distinguish atomicity from retry/idempotency. Prerequisite: [[03-inserting-and-viewing-data]]. Practice: `pg-migration` and `pg-transfer` in [[practice-catalog]]. All destructive examples belong in a disposable database.

Uses the same `owners` / `dogs` model as [[03-inserting-and-viewing-data|Inserting and Viewing Data]].

## UPDATE

```sql
-- One row
UPDATE dogs SET age = 3 WHERE name = 'Gino';

-- Multiple columns
UPDATE dogs SET name = 'Gino Jr.', age = 4 WHERE id = 1;

-- Bulk update with condition
UPDATE dogs SET age = age + 1 WHERE age < 5;
```

- Forgetting `WHERE` updates **every row**. In `psql`, always `SELECT` first with the same `WHERE` to preview.
- `UPDATE ... RETURNING` gives back the changed rows (useful for apps, avoids a second `SELECT`):

```sql
UPDATE dogs SET age = 3 WHERE id = 1 RETURNING id, name, age;
```

## DELETE

```sql
-- One row
DELETE FROM dogs WHERE id = 1;

-- Bulk + preview first
SELECT * FROM dogs WHERE age > 15;
DELETE FROM dogs WHERE age > 15;

-- With RETURNING
DELETE FROM dogs WHERE id = 2 RETURNING *;
```

- No WHERE deletes all rows. TRUNCATE is a different operation with stronger locking, FK restrictions and different trigger behavior. It does not reset sequences unless RESTART IDENTITY is requested:

```sql
TRUNCATE dogs RESTART IDENTITY;
```

- DELETE respects declared FK actions: NO ACTION is default; RESTRICT, CASCADE and SET NULL have different meanings. See [[04-primary-foreign-keys|Primary & Foreign Keys]].

## UPSERT (Insert or Update on Conflict)

Backend staple for retries / syncs / seed scripts. Requires a `UNIQUE` / `PK` target, otherwise: `there is no unique or exclusion constraint`.

Base `owners` / `dogs` tables have no `UNIQUE` on `name` — add it once, then upsert:

```sql
-- One-time setup (see [[09-altering-tables|Altering Tables]])
ALTER TABLE owners ADD CONSTRAINT owners_name_unique UNIQUE (name);

-- Idempotent seed: second run does nothing instead of erroring
INSERT INTO owners (name) VALUES ('Ana')
ON CONFLICT (name) DO NOTHING;

-- Or update on conflict (dogs.id is PK, always works)
INSERT INTO dogs (id, name, age) VALUES (1, 'Gino', 3)
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  age = EXCLUDED.age
RETURNING *;
```

- `EXCLUDED` = the row that failed to insert.
- Bare `ON CONFLICT DO NOTHING` (no target) works without a unique constraint but matches any conflict — prefer explicit `(column)` form.

## Choosing Quickly

| Use this | When |
|---|---|
| `UPDATE ... WHERE` | change existing rows, always with `WHERE` |
| `UPDATE ... RETURNING` | app needs updated row without re-query |
| `DELETE ... WHERE` | remove few rows, FKs enforced |
| `TRUNCATE` | wipe test table fast |
| `ON CONFLICT DO NOTHING` | idempotent inserts / seeds |
| `ON CONFLICT DO UPDATE` | sync / upsert from API |

Pitfalls:
- `UPDATE` / `DELETE` without `WHERE` — #1 data-loss cause.
- PostgreSQL UPDATE has no direct LIMIT clause. A batch can select a bounded key set in a CTE/subquery, then update those keys inside a transaction. Consider concurrent workers, locks, stable ordering and retries rather than blindly copying a range pattern.

## Practice and retrieval

In `pg-migration`, deliberately supply conflicting data and prove the old values and schema survive failure. Explain why SELECT-preview alone is not a concurrency guarantee and why `ON CONFLICT DO NOTHING` does not automatically make a whole business operation idempotent.

Sources: [UPDATE](https://www.postgresql.org/docs/18/sql-update.html), [TRUNCATE](https://www.postgresql.org/docs/18/sql-truncate.html), [INSERT / ON CONFLICT](https://www.postgresql.org/docs/18/sql-insert.html).

## Related Notes

- [[03-inserting-and-viewing-data|Inserting and Viewing Data]]
- [[10-transactions|Transactions]]
- [[08-filtering-sorting-aggregates|Filtering, Sorting & Aggregates]]
