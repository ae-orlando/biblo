---
created: 2026-09-30
updated: 2026-10-21
---

# Indexes & Performance

> Outcome: choose and evaluate an access path for a stated workload. Prerequisites: [[08-filtering-sorting-aggregates]], [[06-table-joining-methods]]. Practice: `pg-plans` in [[practice-catalog]], including its required saved plan interpretation.

## What Gets Indexed Automatically

- PRIMARY KEY and UNIQUE constraints normally create supporting unique B-tree indexes. Other features, such as exclusion constraints, can create indexes too. Foreign key **referencing** columns are not automatically indexed; the referenced key must have an eligible unique supporting index.

Candidate indexes come from actual predicates, joins, order/limit, cardinality, write workload and referential actions. Do not index every filtered column automatically. Consider composite order, partial predicates, included columns, selectivity, table size and update cost; measure the representative query.

```sql
CREATE INDEX IF NOT EXISTS idx_dogs_owner ON dogs (owner_id);

-- Unique + partial (backend favorites)
CREATE UNIQUE INDEX IF NOT EXISTS uq_owners_name ON owners (name);
CREATE INDEX IF NOT EXISTS idx_dogs_adult ON dogs (owner_id) WHERE age >= 2;
```

Drop: `DROP INDEX IF EXISTS idx_dogs_owner;`
List: `\di`, per-table: `\d dogs`.

## EXPLAIN (Is It Using the Index?)

```sql
EXPLAIN SELECT * FROM dogs WHERE owner_id = 1;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM dogs WHERE owner_id = 1;
```

- A sequential scan can be optimal even on a large table when many rows are needed. An index scan can be expensive when it causes many random heap reads. Judge work and selectivity, not the node's name.
- EXPLAIN ANALYZE executes the query, including side effects and locks. Use a disposable environment for practice. ROLLBACK can undo transactional table changes but does not undo sequence advances, external side effects or the operational impact of locks/work; it does not make production experiments universally safe.
- After bulk loads / schema changes: `ANALYZE dogs;` so the planner has fresh stats.

## Backend Pitfalls

1. **N+1 queries:** 1 query for owners + N queries for each owner's dogs. Fix with `JOIN` (see [[06-table-joining-methods|Table Joining Methods]]) or `WHERE owner_id = ANY($1)` batching / ORM `include` / `prefetch`.
2. **`SELECT *` in hot paths:** pulls unused columns, breaks covering indexes. List columns.
3. **Leading `%` kills B-tree:** `WHERE name LIKE '%o%'` can't use a plain index. For search: `pg_trgm` + GIN:
   ```sql
   CREATE EXTENSION IF NOT EXISTS pg_trgm;
   CREATE INDEX idx_dogs_name_trgm ON dogs USING GIN (name gin_trgm_ops);
   ```
4. **Function on indexed column:** `WHERE lower(name) = 'gino'` skips `idx(name)`. Index the expression: `CREATE INDEX ON dogs (lower(name));`
5. **Unindexed FK deletes:** `DELETE FROM owners WHERE id = 1` scans all `dogs` without `idx_dogs_owner` — slow + locks.

## Write Cost

An index helps only eligible queries and costs storage, cache and write maintenance. There is no universal “3–5 indexes per table” limit. A zero idx_scan over an unknown/reset observation window does not prove an index is disposable; check constraint dependencies, rare critical queries, replicas and the time period represented by statistics.

## Read the plan as a tree

Costs are planner units, not milliseconds. Compare estimated versus actual output rows; actual node rows/time are generally per-loop averages, so inspect loops. Distinguish rows scanned from emitted rows, index conditions from residual filters, and a sort eliminated by index order from a sort still required.

BUFFERS describes page activity, not directly elapsed storage latency. Warm caches and statistics change measurements. An index-only scan may still perform heap fetches when visibility information requires them. Explain the plan before proposing an index.

## Practice and retrieval

Complete `pg-plans` with the selective query and a broad query. Save before/after plans, not a promised fixed speedup. Explain how a composite `(user_id,created_at,id)` index fits this workload, why a partial predicate matters, and what extra writes/storage you bought. Extend to cursor pagination and remeasure.

Sources: [Using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html), [indexes](https://www.postgresql.org/docs/18/indexes.html), [statistics views](https://www.postgresql.org/docs/18/monitoring-stats.html).

## Related Notes

- [[04-primary-foreign-keys|Primary & Foreign Keys]]
- [[08-filtering-sorting-aggregates|Filtering, Sorting & Aggregates]]
- [[13-admin-and-ops|Admin & Ops]]
