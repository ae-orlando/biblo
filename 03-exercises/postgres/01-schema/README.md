# Lab: account schema and constraints

**ID:** `pg-schema` · PostgreSQL 15+ · Outcome: enforce a data contract rather than relying on application promises.

Prerequisites: [[02-sql-datatypes]], [[04-primary-foreign-keys]], [[05-relationships]], [[14-schema-design-and-null]]. No system database setup is needed; the checker starts the isolated vault cluster.

## Contract

Implement `work/answer.sql`:
- `users`: generated `bigint` primary key `id`, unique non-null `email`, `created_at timestamptz` defaulting to now.
- An email must be nonempty and already trimmed/lowercase. This is a canonicalization exercise, **not** a complete email validator or proof of deliverability.
- `profiles`: exactly one possible profile per `user_id`, non-null `display_name`. A user may have zero profiles.
- `login_events`: generated key, required existing `user_id`, required `succeeded boolean`, timestamp defaulting to now. Many events may reference one user.
- Deleting a user removes its profile and events **for this exercise**. Explain why an actual audit log might require a different retention policy.

## Attempt and check

```bash
python3 90-tools/practice.py start pg-schema
python3 90-tools/practice.py check pg-schema
```

Tests create and drop uniquely named databases in the vault cluster. They verify valid inserts first, then duplicate, NULL, malformed, orphan and delete cases. A starter that creates no tables fails.

## Completion and transfer

Draw cardinalities, predict each constraint error, and explain why `CHECK` alone does not replace `NOT NULL`. Extend the schema to support multiple email addresses without permitting duplicate addresses across users; write new regression cases.

[Progressive hints](hints.md) · [Separate reference explanation](../../../07-solutions/pg-schema/explanation.md) · [PostgreSQL constraints](https://www.postgresql.org/docs/18/ddl-constraints.html)
