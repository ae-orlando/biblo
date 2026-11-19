---
created: 2026-09-30
updated: 2026-10-21
---

# Filtering, Sorting & Aggregates

> Outcome: place filters correctly and explain what each count includes. Prerequisites: [[03-inserting-and-viewing-data]], [[14-schema-design-and-null]]. Practice: `pg-queries` in [[practice-catalog]].

Read companion: [[03-inserting-and-viewing-data|Inserting and Viewing Data]] for basic `SELECT`.

## WHERE (Backend Filters)

```sql
SELECT name, age FROM dogs
WHERE age >= 2 AND age <= 5;

SELECT * FROM dogs WHERE name IN ('Gino', 'Nora');
SELECT * FROM dogs WHERE age BETWEEN 2 AND 5;
SELECT * FROM dogs WHERE owner_id IS NULL;      -- strays
SELECT * FROM dogs WHERE owner_id IS NOT NULL;  -- owned

-- Pattern matching
SELECT * FROM dogs WHERE name LIKE 'G%';   -- case-sensitive, G...
SELECT * FROM dogs WHERE name ILIKE 'g%';  -- case-insensitive (Postgres-only)
SELECT * FROM dogs WHERE name LIKE '%o%';  -- contains 'o'
```

- `= NULL` never matches — always `IS NULL` / `IS NOT NULL`.
- `AND` beats `OR` — parenthesize: `WHERE (age < 2 OR age > 10) AND owner_id IS NULL`.
- `NOT IN` with `NULL` in the list returns no rows — prefer `NOT EXISTS` (see [[12-subqueries-ctes-views|Subqueries, CTEs & Views]]).

## ORDER BY, LIMIT, OFFSET

```sql
SELECT name, age FROM dogs ORDER BY age DESC;
SELECT name, age FROM dogs ORDER BY age DESC, name ASC;

-- Pagination (backend staple)
SELECT * FROM dogs ORDER BY id LIMIT 20 OFFSET 40; -- page 3, size 20

-- Be explicit with NULLS FIRST/LAST for stable APIs
SELECT name, owner_id FROM dogs ORDER BY owner_id NULLS LAST;
```

Default in Postgres: `ASC` puts `NULLS LAST`, `DESC` puts `NULLS FIRST`. Be explicit with `NULLS FIRST/LAST` for APIs.

- Use a uniquely determined order, such as `(created_at,id)`, for deterministic pagination. Concurrent changes can still shift OFFSET pages; see [[15-window-functions-and-pagination]].

## DISTINCT

```sql
SELECT DISTINCT owner_id FROM dogs; -- unique owner ids (includes NULL once)
SELECT COUNT(DISTINCT owner_id) FROM dogs;
```

## Aggregates

```sql
SELECT COUNT(*) FROM dogs;            -- all rows
SELECT COUNT(owner_id) FROM dogs;     -- non-NULL only
SELECT AVG(age), MIN(age), MAX(age), SUM(age) FROM dogs;
```

- COUNT(column) and the common scalar SUM/AVG/MIN/MAX aggregates ignore NULL inputs; COUNT(*) counts rows. This is not a rule for every aggregate (array_agg, for example, includes NULL values).
- `SELECT name, COUNT(*)` without `GROUP BY` is an error — bare columns must be grouped.

## GROUP BY + HAVING

`WHERE` filters rows **before** grouping, `HAVING` filters groups **after**.

```sql
-- Dogs per owner
SELECT owner_id, COUNT(*) AS dog_count, AVG(age) AS avg_age
FROM dogs
GROUP BY owner_id;

-- Only owners with 2+ dogs
SELECT owner_id, COUNT(*) AS dog_count
FROM dogs
GROUP BY owner_id
HAVING COUNT(*) >= 2;

-- Full pipeline order: WHERE -> GROUP BY -> HAVING -> ORDER BY -> LIMIT
SELECT owner_id, COUNT(*) AS n
FROM dogs
WHERE age >= 1
GROUP BY owner_id
HAVING COUNT(*) >= 1
ORDER BY n DESC
LIMIT 10;
```

## Choosing Quickly

| Use this | When |
|---|---|
| `WHERE` | filter rows |
| `ORDER BY id LIMIT/OFFSET` | API pagination |
| `DISTINCT` | dedupe small result |
| `COUNT/AVG/MIN/MAX/SUM` | stats |
| `GROUP BY + HAVING` | per-group stats, filter on aggregate |
| `ILIKE` | case-insensitive search (small tables; trigram index for large, see [[11-indexes-and-performance|Indexes & Performance]]) |

## Related Notes

- [[03-inserting-and-viewing-data|Inserting and Viewing Data]]
- [[06-table-joining-methods|Table Joining Methods]]
- [[11-indexes-and-performance|Indexes & Performance]]

## Practice and retrieval

Use `pg-queries` to compare COUNT(*) with COUNT(login.id) after a left join. Predict empty-input SUM versus COUNT, then test. Extend to users with at least two successful logins without accidentally dropping users in a separate all-users report. Explain WHERE versus HAVING and why output order must be explicit.

Sources: [Aggregates](https://www.postgresql.org/docs/18/functions-aggregate.html), [table expressions](https://www.postgresql.org/docs/18/queries-table-expressions.html).
