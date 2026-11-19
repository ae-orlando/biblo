---
created: 2026-09-26
updated: 2026-10-21
---

# SQL Datatypes (Postgres)

> Outcome: choose types based on domain/range/precision, not habit. Prerequisite: [[00-postgres-introduction]]. Practice: `pg-schema` in [[practice-catalog]]. SQL column lists below are fragments; the lab defines a complete schema.

When creating tables in SQL, each column must have a datatype plus optional constraints:

```sql
CREATE TABLE table_name(
  column1 data_type column_constraint,
  column2 data_type column_constraint,
  column3 data_type column_constraint
);
```

Example: `id SERIAL PRIMARY KEY` = integer type + auto-increment + primary key constraint.

## 1. Numeric

### a. Integers

- `INT` / `INTEGER` takes up 4 bytes, range -2,147,483,648 to 2,147,483,647.
- Variants:
  - `SMALLINT` — 2 bytes, -32,768 to 32,767.
  - `INT` / `INTEGER` — 4 bytes (standard choice for ids/counts).
  - `BIGINT` — 8 bytes, up to ~9.2 quintillion. Use for large counters.
  - `SMALLSERIAL`, `SERIAL`, `BIGSERIAL` — not true types; auto-incrementing `SMALLINT` / `INT` / `BIGINT`. Legacy shorthand — prefer `GENERATED ... AS IDENTITY` in new code (Postgres 10+).

```sql
id SERIAL PRIMARY KEY,
age SMALLINT CHECK (age >= 0)
```

### b. Exact / Approximate Numbers

- `NUMERIC(p,s)` / `DECIMAL(p,s)` — exact, arbitrary precision. Use for money. Example: `NUMERIC(10,2)` = 10 digits total, 2 after decimal.
- `REAL` — 4-byte float, 6 decimal digits precision.
- `DOUBLE PRECISION` — 8-byte float, 15 decimal digits precision. Use for scientific measurements, never for money.

```sql
price NUMERIC(10,2) NOT NULL,
rating REAL
```

## 2. Text

- `CHAR(n)` — fixed length, blank-padded. Rare; use for codes like `CHAR(2)` country codes.
- `VARCHAR(n)` — variable length with limit. Example: `VARCHAR(255)` for names.
- `TEXT` — variable length, unlimited. Preferred in Postgres unless you need a hard limit (performance is the same as `VARCHAR`).

```sql
username VARCHAR(50) UNIQUE NOT NULL,
bio TEXT
```

## 3. Boolean

- `BOOLEAN` (alias `BOOL`). Values: `TRUE` / `FALSE`, also accepts `1/0`, `'yes'/'no'`, `'t'/'f'`.

```sql
is_active BOOLEAN DEFAULT TRUE
```

## 4. Date & Time

| Type | Stores | Example |
|---|---|---|
| `DATE` | calendar date | `2026-09-28` |
| `TIME` | time of day | `14:30:00` |
| `TIMESTAMP` | date + time, no timezone | `2026-09-28 14:30:00` |
| `TIMESTAMPTZ` | an instant, displayed in the session timezone; original zone name is not retained | `2026-09-28 14:30:00+00` |
| `INTERVAL` | time span | `7 days`, `1 hour` |

- Prefer `TIMESTAMPTZ` for created/updated columns — avoids timezone bugs.
- Handy defaults: `DEFAULT NOW()`, `DEFAULT CURRENT_DATE`.

```sql
created_at TIMESTAMPTZ DEFAULT NOW(),
birth_date DATE
```

## 5. Other Common Types

- `UUID` — 128-bit identifier. `gen_random_uuid()` is built in on PostgreSQL 13+; pgcrypto is not required there. Random IDs reduce predictability but never replace authorization.
- `JSON` / `JSONB` — semi-structured data. Prefer `JSONB` (indexed, queryable).

```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
meta JSONB
```

## 6. Full Example

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  age SMALLINT CHECK (age >= 0),
  balance NUMERIC(10,2) DEFAULT 0.00,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

Rule of thumb: `TEXT` for free text, `VARCHAR(n)` for bounded input, `INT`/`BIGINT` for counts, `NUMERIC` for money, `TIMESTAMPTZ` for timestamps, `BOOLEAN` for flags.

## Practice and retrieval

In `pg-schema`, defend every column's type, nullability and default. Predict what happens to a value outside an integer range or numeric precision. Explain why a birth date is not an instant, why timestamptz does not preserve “Africa/Nairobi” as a named zone, and why a numeric type alone does not prohibit negative balances.

Sources: [Data types](https://www.postgresql.org/docs/18/datatype.html), [UUID functions](https://www.postgresql.org/docs/18/functions-uuid.html), [date/time](https://www.postgresql.org/docs/18/datatype-datetime.html).

## Related Notes

- [[03-inserting-and-viewing-data|Inserting and Viewing Data]]
- [[04-primary-foreign-keys|Primary & Foreign Keys]]
- [[09-altering-tables|Altering Tables]]
