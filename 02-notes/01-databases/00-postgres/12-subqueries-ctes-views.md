---
created: 2026-09-30
updated: 2026-10-21
---

# Subqueries, CTEs & Views

> Outcome: express intermediate relationships clearly without assuming one syntax is inherently faster. Prerequisites: [[06-table-joining-methods]], [[08-filtering-sorting-aggregates]]. Practice: `pg-queries` in [[practice-catalog]].

## Subqueries

```sql
-- Scalar: one value
SELECT * FROM dogs WHERE age > (SELECT AVG(age) FROM dogs);

-- IN list
SELECT * FROM dogs WHERE owner_id IN (SELECT id FROM owners WHERE name IN ('Ana','Ben'));

-- EXISTS (prefer over NOT IN when NULLs possible)
SELECT o.name FROM owners o
WHERE EXISTS (SELECT 1 FROM dogs d WHERE d.owner_id = o.id);

-- Childless owners (anti-join, alternative to LEFT JOIN ... IS NULL)
SELECT o.name AS childless
FROM owners o
WHERE NOT EXISTS (SELECT 1 FROM dogs d WHERE d.owner_id = o.id);
```

- `IN` + `NULL` in subquery breaks `NOT IN` — use `NOT EXISTS`.
- A correlated subquery references the outer query. Depending on its form and optimizer transformations, it may use a per-row subplan or be transformed into another plan. Do not prescribe a JOIN rewrite based only on syntax; compare results and representative EXPLAIN plans.

## CTEs (WITH) — Readability for Backend Queries

```sql
WITH adult_dogs AS (
  SELECT * FROM dogs WHERE age >= 2
),
owner_counts AS (
  SELECT owner_id, COUNT(*) AS n FROM adult_dogs GROUP BY owner_id
)
SELECT o.name, c.n
FROM owners o JOIN owner_counts c ON c.owner_id = o.id
ORDER BY c.n DESC;
```

- Use CTEs to name intermediate steps instead of nested subqueries.
- PostgreSQL 12+ can fold eligible side-effect-free nonrecursive CTEs into the parent query; reference count and other properties matter. MATERIALIZED/NOT MATERIALIZED can influence eligible cases. Inspect the actual plan instead of treating CTEs as always an optimization fence or always inlined.

## Views (Saved Queries)

```sql
CREATE VIEW dogs_with_owners AS
SELECT d.id, d.name AS dog, d.age, o.name AS owner
FROM dogs d LEFT JOIN owners o ON o.id = d.owner_id;

SELECT * FROM dogs_with_owners WHERE age >= 2;
DROP VIEW IF EXISTS dogs_with_owners;
```

- Views are stored queries, not stored data — always fresh, no extra storage.
- Use for stable API shapes / hiding joins. For heavy aggregates polled often, consider `MATERIALIZED VIEW` + `REFRESH MATERIALIZED VIEW` (stale until refreshed).
- Don't stack views on views — debugging gets painful.

## UNION (Stack Results)

```sql
SELECT name FROM owners
UNION        -- dedupes
SELECT name FROM dogs
ORDER BY 1;

SELECT name FROM owners
UNION ALL    -- keeps dupes, faster
SELECT name FROM dogs;
```

- Columns must match in count/type. `UNION` dedupes (sort cost), `UNION ALL` is faster when dupes are fine.

## Choosing Quickly

| Use this | When |
|---|---|
| `EXISTS / NOT EXISTS` | membership, NULL-safe |
| CTE (`WITH`) | multi-step readable query |
| View | reused join/shape across app |
| Materialized view | expensive report, tolerate staleness |
| `UNION ALL` | combine same-shape results fast |

## Related Notes

- [[06-table-joining-methods|Table Joining Methods]]
- [[08-filtering-sorting-aggregates|Filtering, Sorting & Aggregates]]
- [[05-relationships|Relationships]]

## Practice and retrieval

Implement the absence and latest-event reports in `pg-queries`. Compare NOT EXISTS with a correctly formulated left anti-join, including NULL data. Explain why UNION ALL has different semantics from UNION, why a view does not promise row order, and when refresh staleness is acceptable for a materialized view.

Sources: [WITH queries](https://www.postgresql.org/docs/18/queries-with.html), [subquery expressions](https://www.postgresql.org/docs/18/functions-subquery.html), [views](https://www.postgresql.org/docs/18/sql-createview.html).
