---
created: 2026-09-26
updated: 2026-10-21
---

# Primary & Foreign Keys

> Outcome: distinguish identity, business uniqueness and referential integrity. Prerequisite: [[02-sql-datatypes]]. Practice: `pg-schema` in [[practice-catalog]].

They are the basis of relationships in relational databases.

## Primary Keys

A column or set of columns that uniquely identifies each record.
- Cannot be `NULL`.
- Must be unique — Postgres creates a B-tree index behind it.

To make a column a primary key:

```sql
column_name data_type PRIMARY KEY
```

Example (see [[03-inserting-and-viewing-data|Inserting and Viewing Data]]):

```sql
CREATE TABLE dogs (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);
```

## Composite Primary Key

Two or more columns together act as the key. Declared at the table level:

```sql
CREATE TABLE enrollment (
  student_id INTEGER NOT NULL,
  course_id INTEGER NOT NULL,
  enrolled_on DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (student_id, course_id)
);
```

Choose based on identity and referencing needs. A composite primary key is often appropriate for a junction. A surrogate ID does not remove the need for a UNIQUE constraint on a naturally unique pair.

## Foreign Keys

A column or column set referencing an eligible unique key, often another table's primary key. It enforces referential integrity for non-null references; it does not imply NOT NULL or require the referenced column to be named `id`.

```sql
CREATE TABLE owners (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE dogs (
  id SERIAL PRIMARY KEY,
  owner_id INTEGER NOT NULL REFERENCES owners (id) ON DELETE CASCADE,
  name VARCHAR(50) NOT NULL
);
```

- `REFERENCES owners (id)` = this column must match an existing `owners.id`.
- `ON DELETE CASCADE` deletes matching child rows. Default is `NO ACTION`, not RESTRICT. NO ACTION can permit a deferred check when the constraint is deferrable; RESTRICT cannot defer that action. SET NULL requires the affected columns to permit NULL. Choose by retention/business rules, not convenience.

Inline vs table-level syntax (equivalent):

```sql
-- Table-level, better for composite FKs
FOREIGN KEY (owner_id) REFERENCES owners (id) ON DELETE CASCADE
```

## Joining on Keys

```sql
SELECT d.name AS dog, o.name AS owner
FROM dogs d
JOIN owners o ON o.id = d.owner_id;
```

## Related Notes

- [[05-relationships|Relationships]]
- [[06-table-joining-methods|Table Joining Methods]]
- [[11-indexes-and-performance|Indexes & Performance]]

## Practice and retrieval

Use `pg-schema` to violate PK/UNIQUE/FK/NOT NULL independently. Explain why a nullable FK still permits an unassigned relationship and why a foreign key does not automatically index its referencing columns. Change the delete rule and predict the failure or retained data before testing.

Sources: [Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html).
