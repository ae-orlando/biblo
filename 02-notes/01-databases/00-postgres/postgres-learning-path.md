# PostgreSQL learning path

## Prerequisites and environment

Use [[baseline-diagnostic]] to place yourself. Learn a terminal's working directory, stdin/stdout and process status first if necessary. You do not need a framework, Docker or a system PostgreSQL service.

The labs use `90-tools/postgres.py`: a disposable cluster under `.practice-runtime/postgres/`, loopback TCP disabled, private Unix socket, fake data, and explicit connection arguments. Tests create/drop only uniquely named databases in this cluster. See [[vault-maintenance]] for stop/recovery commands.

Do not paste every lesson's alternative `CREATE TABLE` example into one database. The owners/dogs examples are small illustrations; lab fixtures define their own exact schemas. Use `90-tools/demo-dogs.sql` for a coherent manual demo in a scratch database.

## Sequence and gates

| Unit | Read | Practice / demonstrated outcome |
| --- | --- | --- |
| Orient | [[00-postgres-introduction]], [[01-psql-workflow]] | Identify server/cluster/database/schema/role; connect to the intended isolated instance |
| Model | [[02-sql-datatypes]], [[04-primary-foreign-keys]], [[05-relationships]], [[14-schema-design-and-null]] | `pg-schema`: defend types, keys, nullability, cardinality and delete behavior |
| Read/write | [[03-inserting-and-viewing-data]], [[07-updating-and-deleting-data]], [[08-filtering-sorting-aggregates]] | Predict changed rows; verify output and invariants, not just command status |
| Query | [[06-table-joining-methods]], [[12-subqueries-ctes-views]], [[15-window-functions-and-pagination]] | `pg-queries`: retain zero-event users and break ties deterministically |
| Evolve | [[09-altering-tables]], [[10-transactions]] | `pg-migration`: valid backfill and all-or-nothing failure |
| Contend | [[16-concurrency-and-application-sql]] | `pg-transfer`: preserve balances with concurrent callers |
| Measure | [[11-indexes-and-performance]] | `pg-plans`: correct index plus saved before/after interpretation |
| Operate | [[13-admin-and-ops]] | `pg-restore`: effective least privilege and tested separate restore |

Find specifications in [[practice-catalog]]. Each has unfinished starter code, behavioral checks, hints, and a separate reference explanation.

## Cumulative checkpoint

Design a small booking or inventory system from a written business brief. Include an optional relationship, a many-to-many relationship, a nonnegative quantity and a uniqueness rule. Produce schema, seed data, reports, a failure-safe multirow operation, migration, measured query plan and restore evidence.

Then accept a change: simultaneous bookings must never oversell, retries must not duplicate a completed booking, and users with no activity must still appear in reports. Explain transaction and idempotency boundaries separately. Use [[study-and-review]]; a passing toy schema is not production-readiness evidence.

For the selected Python backend direction, continue into [[fastapi-learning-path]]'s persistence unit after Python/HTTP prerequisites. Existing Django/project documents are optional references, not the curriculum's destination.
