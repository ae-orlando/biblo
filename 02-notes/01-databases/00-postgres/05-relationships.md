---
created: 2026-09-26
updated: 2026-10-21
---

# Relationships

> Outcome: encode cardinality and explain optionality. Prerequisite: [[04-primary-foreign-keys]]. Practice: `pg-schema`, followed by `pg-queries`, in [[practice-catalog]]. Examples are alternative models, not DDL to paste sequentially.

The relational model represents data as relations (commonly tables), not merely links between tables. Foreign keys express referential constraints; cardinality describes how many rows on each side may match.

There are 3 real types (+ 1 special case):

1. One-to-Many (includes Many-to-One — same link, opposite viewpoint)
2. One-to-One
3. Many-to-Many (needs a junction table)
4. Self-referencing (a table referencing itself)

## 1. One-to-Many / Many-to-One

The most common. One parent has many children; each child belongs to one parent. The FK lives on the "many" side.

Example: one `owner` has many `dogs`:

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

Query:

```sql
SELECT d.name AS dog, o.name AS owner
FROM dogs d
JOIN owners o ON o.id = d.owner_id;
```

- Many-to-One is the same link read backwards: many `dogs` → one `owner`.

## 2. One-to-One

One row matches at most one row in the other table. Implement as a FK with a `UNIQUE` constraint so the child can't repeat.

Example: each `dog` has at most one `medical_record`:

```sql
CREATE TABLE medical_records (
  id SERIAL PRIMARY KEY,
  dog_id INTEGER UNIQUE NOT NULL REFERENCES dogs (id) ON DELETE CASCADE,
  blood_type VARCHAR(5),
  notes TEXT
);
```

- `UNIQUE` on `dog_id` is what makes it 1-to-1 instead of 1-to-many.
- Alternative: share the PK (`id INTEGER PRIMARY KEY REFERENCES dogs (id)`), but the `UNIQUE FK` form above is more explicit.
- Use sparingly — for splitting a rarely-used or sensitive subset of columns. Otherwise just add columns to the base table.

## 3. Many-to-Many

Many rows on each side match many on the other. Needs a junction (join) table with two FKs. The pair is usually the composite PK, which also blocks duplicates.

**Composite PK** = two or more columns combined to uniquely identify each row.

Example: `dogs` learn many `tricks`, each `trick` is known by many `dogs`:

```sql
CREATE TABLE tricks (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE dog_tricks (
  dog_id INTEGER NOT NULL REFERENCES dogs (id) ON DELETE CASCADE,
  trick_id INTEGER NOT NULL REFERENCES tricks (id) ON DELETE CASCADE,
  taught_on DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (dog_id, trick_id)
);
```

Query:

```sql
SELECT d.name AS dog, t.name AS trick
FROM dogs d
JOIN dog_tricks dt ON dt.dog_id = d.id
JOIN tricks t ON t.id = dt.trick_id
ORDER BY d.name;
```

## 4. Self-Referencing

A FK points back to the same table. Models hierarchies.

Example: an employee's manager is also an employee:

```sql
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  manager_id INTEGER REFERENCES employees (id) ON DELETE SET NULL
);
```

- `manager_id` must be nullable — the top row has no manager.
- Same pattern: `categories(parent_id)`, `comments(parent_id)`, `dogs(mother_id)`.

Query with a self-join (alias the table twice):

```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```

- `LEFT JOIN` keeps top-level rows with no manager.

## Choosing Quickly

| Use this | When | How |
|---|---|---|
| One-to-Many | parent owns children | FK on child table |
| One-to-One | one-to-one extension | FK + `UNIQUE` |
| Many-to-Many | both sides repeat | junction table, composite PK |
| Self-referencing | hierarchy in one entity | FK to own PK, nullable |

Rule of thumb: start with One-to-Many. Reach for a junction table only when both sides genuinely repeat. Reach for One-to-One only to split a table, not to model ownership.

## Practice and retrieval

Draw the users/profiles/login_events schema before implementing `pg-schema`. Annotate zero/one/many at both ends. Explain why a unique FK enforces “at most one,” not “every user must have one.” Extend with user/group membership and prevent duplicate membership with a pair constraint.

Sources: [Constraints and foreign keys](https://www.postgresql.org/docs/18/ddl-constraints.html).

## Related Notes

- [[04-primary-foreign-keys|Primary & Foreign Keys]]
- [[06-table-joining-methods|Table Joining Methods]]
- [[03-inserting-and-viewing-data|Inserting and Viewing Data]]
