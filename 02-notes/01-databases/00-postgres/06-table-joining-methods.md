---
created: 2026-09-26
updated: 2026-10-21
---

# Table Joining Methods

> Outcome: predict matching and null-extended rows, then test reports against missing and duplicate relationships. Prerequisite: [[05-relationships]]. Practice: `pg-queries` in [[practice-catalog]].

SQL's `JOIN` combines rows from different tables via a shared key — usually `FK = PK` (see [[04-primary-foreign-keys|Primary & Foreign Keys]]).

`OUTER` is optional: `LEFT JOIN` = `LEFT OUTER JOIN`. `JOIN` alone means `INNER JOIN`.

## Demo Data

Same `owners` / `dogs` model as [[05-relationships|Relationships]], but `owner_id` is nullable so outer joins have something to show:

```sql
CREATE TABLE owners (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE dogs (
  id SERIAL PRIMARY KEY,
  owner_id INTEGER REFERENCES owners (id) ON DELETE SET NULL,
  name VARCHAR(50) NOT NULL
);

INSERT INTO owners (name) VALUES ('Ana'), ('Ben'), ('Cara');
-- Ana id=1, Ben id=2, Cara id=3 (Cara has no dogs)

INSERT INTO dogs (name, owner_id) VALUES
  ('Gino', 1), ('Nora', 1), ('Milo', NULL);
-- Milo is a stray (no owner)
```

## 1. INNER JOIN

Only rows with a match on **both** sides. The default — use when orphans should be excluded.

```sql
SELECT d.name AS dog, o.name AS owner
FROM dogs d
JOIN owners o ON o.id = d.owner_id;
```

| dog | owner |
|---|---|
| Gino | Ana |
| Nora | Ana |

- `Milo` (no owner) and `Cara` (no dogs) are dropped.
- Use for junction queries too (see `dog_tricks` in [[05-relationships|Relationships]]).

## 2. LEFT OUTER JOIN

All rows from the **left** table + matches from the right. Non-matches get `NULL`.

```sql
-- All dogs, with owner where known
SELECT d.name AS dog, o.name AS owner
FROM dogs d
LEFT JOIN owners o ON o.id = d.owner_id;
```

| dog | owner |
|---|---|
| Gino | Ana |
| Nora | Ana |
| Milo | NULL |

Anti-join pattern — find orphans (strays with no owner):

```sql
SELECT d.name AS stray
FROM dogs d
LEFT JOIN owners o ON o.id = d.owner_id
WHERE o.id IS NULL;
```

## 3. RIGHT OUTER JOIN

Mirror of `LEFT JOIN`: all rows from the **right** table. Rarely written — flip the tables and use `LEFT JOIN` instead.

```sql
-- Equivalent: prefer the LEFT JOIN form
SELECT d.name AS dog, o.name AS owner
FROM owners o
LEFT JOIN dogs d ON d.owner_id = o.id;
-- vs.
SELECT d.name AS dog, o.name AS owner
FROM dogs d
RIGHT JOIN owners o ON o.id = d.owner_id;
```

| dog | owner |
|---|---|
| Gino | Ana |
| Nora | Ana |
| NULL | Ben |
| NULL | Cara |

- Shows childless owners (`Ben`, `Cara`). Rule: if you see `RIGHT JOIN`, rewrite as `LEFT JOIN` for readability.

## 4. FULL OUTER JOIN

All rows from **both** tables. `NULL` wherever either side has no match.

```sql
SELECT d.name AS dog, o.name AS owner
FROM dogs d
FULL JOIN owners o ON o.id = d.owner_id
ORDER BY dog NULLS LAST, owner;
```

| dog | owner |
|---|---|
| Gino | Ana |
| Milo | NULL |
| Nora | Ana |
| NULL | Ben |
| NULL | Cara |

- Use for reconciliation reports ("what's missing on either side?"). Rare in app queries.

## 5. CROSS JOIN

Cartesian product: every row × every row. No `ON` clause.

```sql
SELECT d.name AS dog, t.name AS trick
FROM dogs d
CROSS JOIN tricks t;
```

- 3 dogs × 4 tricks = 12 rows. Explodes fast — double-check row counts before running on big tables.
- Uses: generating combinations, test data, matrix reports.
- An ordinary qualified INNER/LEFT join without ON, USING or NATURAL is a syntax error in PostgreSQL. A CROSS JOIN, comma join without a restricting condition, or `JOIN ... ON true` produces a Cartesian product. A valid but incomplete condition can also multiply rows unexpectedly; check cardinality and predicates.

## 6. SELF JOIN

Not a keyword — an `INNER/LEFT JOIN` of a table to itself with two aliases. For hierarchies (see [[05-relationships|Relationships]] §4).

```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```

- Must alias (`e`, `m`); otherwise column references are ambiguous.
- Use `LEFT JOIN` so top-level rows (no manager) are kept.

## Choosing Quickly

| Use this | Keeps | Drops |
|---|---|---|
| `JOIN` (inner) | matches only | orphans both sides |
| `LEFT JOIN` | all left rows | unmatched right |
| `RIGHT JOIN` | all right rows | prefer `LEFT JOIN` flipped |
| `FULL JOIN` | all rows both sides | nothing |
| `CROSS JOIN` | every combination | — (no `ON`) |
| Self-join | hierarchy pairs | depends on inner vs left |

Pitfalls:
- Filtering an outer join in `WHERE` (e.g. `WHERE o.name = 'Ana'`) drops the `NULL` rows and silently turns it into an inner join — move the filter into the `ON` if you want to keep them.
- `ON` vs `USING`: `JOIN ... USING (owner_id)` works when both columns share the name, and merges them into one output column. `ON` is more explicit and works always.

## Related Notes

- [[05-relationships|Relationships]]
- [[04-primary-foreign-keys|Primary & Foreign Keys]]
- [[12-subqueries-ctes-views|Subqueries, CTEs & Views]]

## Practice and retrieval

Before running `pg-queries`, draw the rows kept by INNER versus LEFT joins. Count a non-null event key instead of COUNT(*) when reporting zero related rows. Add a right-side filter in WHERE, observe the lost unmatched users, then move it to the appropriate input/ON clause and explain the changed meaning.

Sources: [Table expressions and joins](https://www.postgresql.org/docs/18/queries-table-expressions.html).
