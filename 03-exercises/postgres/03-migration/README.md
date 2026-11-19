# Lab: atomic data cleanup and schema migration

**ID:** `pg-migration` · Outcome: strengthen an invariant without leaving a partial migration after failure.

Prerequisites: [[07-updating-and-deleting-data]], [[09-altering-tables]], [[10-transactions]], [[14-schema-design-and-null]].

## Starting state and contract

The checker creates `contacts(id integer PRIMARY KEY, email text)` with existing mixed-case/padded values. In `work/answer.sql`, preserve rows and IDs, trim/lowercase emails, then enforce unique, non-null, nonempty, canonical values on future writes.

Use one transaction. When normalization reveals conflicting existing emails, fail and leave **both data and schema** unchanged. Do not silently discard or merge records. A separate business decision is needed to resolve conflicts.

Example: `' ANA@example.test '` becomes `'ana@example.test'`. Two existing rows that both normalize to this value must cause the migration to roll back.

```bash
python3 90-tools/practice.py start pg-migration
python3 90-tools/practice.py check pg-migration
```

Tests run a valid dataset and a conflicting dataset in separate disposable databases. They check the preserved original value and nullability after failure.

## Completion and transfer

Explain lock duration and why this small-table transaction is not a zero-downtime migration recipe. Propose an expand/backfill/validate/contract sequence for a large table and a compatible application deployment. Describe rollback before and after new application writes.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/pg-migration/explanation.md) · [ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html)
