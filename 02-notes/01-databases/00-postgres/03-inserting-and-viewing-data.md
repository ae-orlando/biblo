---
created: 2026-09-26
updated: 2026-10-21
---

# Inserting and Viewing Data

> Outcome: insert explicit fields and verify selected values, not just command success. Prerequisites: [[01-psql-workflow]], [[02-sql-datatypes]]. Practice: `pg-schema` and `pg-queries` in [[practice-catalog]]. Alternative demo DDL is not a sequential migration; see [[postgres-learning-path]].

Let's assume we are in `psql` and create a `dogs` table:
```sql
CREATE TABLE dogs(
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  age INTEGER CHECK (age >= 0)
);
```

## Inserting Data into the Dogs Table

Since `id` auto-increments, insert only the other columns:
```sql
INSERT INTO dogs (name, age)
VALUES ('Gino', 2), ('Nora', 3);
```

- Use single quotes for string literals (`'Gino'`). Double quotes mean identifiers in Postgres.
- You can omit the column list, but specifying columns is safer (survives schema changes):

```sql
-- Fragile: depends on column order
INSERT INTO dogs VALUES (DEFAULT, 'Milo', 1);
```

## Viewing Data

```sql
-- All rows and columns
SELECT * FROM dogs;

-- Specific columns + filter + sort
SELECT name, age FROM dogs
WHERE age >= 2
ORDER BY age DESC;
```

Handy `psql` helpers:

```psql
\d dogs        -- describe table structure
\dt            -- list tables
\x on          -- expanded display for wide rows
``` 

## Practice and retrieval

Predict the generated IDs and returned rows, but do not rely on IDs being gapless or on SELECT without ORDER BY returning insertion order. Add `RETURNING id,name` to an insert and compare it with a later ordered query. In the schema lab, show that an invalid insert fails for the intended constraint, not because the table was never created.

Sources: [INSERT](https://www.postgresql.org/docs/18/sql-insert.html), [select lists](https://www.postgresql.org/docs/18/queries-select-lists.html).

## Related Notes

- [[02-sql-datatypes|SQL Datatypes]]
- [[07-updating-and-deleting-data|Updating and Deleting Data]]
- [[08-filtering-sorting-aggregates|Filtering, Sorting & Aggregates]]
