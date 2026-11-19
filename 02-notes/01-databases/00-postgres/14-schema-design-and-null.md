# Schema design, normalization and NULL

## Outcome and prerequisites

After [[02-sql-datatypes]] and [[04-primary-foreign-keys]], turn a business rule into a schema invariant and explain which invalid states remain possible. Practice: `pg-schema` and `pg-migration` in [[practice-catalog]].

## Model the rule before the columns

Write the entities, attributes, candidate keys and relationship cardinalities. Distinguish “must have exactly one” from “may have at most one.” A unique profile FK enforces at most one profile per user, not that every user has a profile.

Normalization starts with dependencies: an attribute should describe the key, not redundantly describe another entity. Storing owner email on every dog creates update anomalies; reference the owner. A many-to-many relationship needs a junction with a uniqueness rule on the pair. Denormalize only for an explicit measured requirement, with an update-consistency policy.

Choose types by semantics: exact integer minor units or appropriately bounded numeric for money, timestamptz for instants, date for calendar dates, text for free text. Surrogate IDs do not remove the need to enforce business uniqueness. Names usually are not unique identities.

## NULL means missing/unknown, not an empty string or zero

SQL predicates use true, false and unknown. `WHERE` retains only true. `CHECK` rejects false, so `CHECK(age >= 0)` still permits NULL; use `NOT NULL` when the value is required.

```sql
SELECT NULL = NULL, NULL IS NULL, 3 NOT IN (1, NULL);
-- NULL | true | NULL
```

Use `IS NULL` for missing values and `IS [NOT] DISTINCT FROM` for null-safe comparison. `COUNT(*)` counts rows; `COUNT(column)` counts non-null values. Most ordinary scalar aggregates ignore NULL; do not generalize this to every aggregate (for example, array_agg includes NULL inputs).

PostgreSQL UNIQUE normally permits multiple NULLs. PostgreSQL 15+ supports `UNIQUE NULLS NOT DISTINCT` when missing values must compare as duplicates. Choose intentionally.

## Practice and retrieval

Predict whether a missing, blank, duplicate or noncanonical email passes each independent constraint in `pg-schema`. Add a business rule and test both valid and invalid writes directly, not only through a form.

Teach back: why does a foreign key not imply NOT NULL? Why is a unique surrogate key insufficient to prevent duplicate registrations? What normalization problem would copying a profile field into each login event introduce—and when might an immutable event snapshot be intentional?

Sources: [Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html), [comparison functions](https://www.postgresql.org/docs/18/functions-comparison.html), [aggregate functions](https://www.postgresql.org/docs/18/functions-aggregate.html). Lab executions are recorded separately from this explanatory reference.
