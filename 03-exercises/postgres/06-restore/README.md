# Lab: least privilege and demonstrated recovery

**ID:** `pg-restore` · Outcome: prove both denied operations and a usable restored database.

Prerequisites: [[01-psql-workflow]], [[13-admin-and-ops]], [[16-concurrency-and-application-sql]].

## Contract

The checker creates a database containing `notes(id identity PRIMARY KEY, body text NOT NULL)` and two rows. It passes psql identifier variables `:"reader"` and `:"database"` to `work/answer.sql`.

Create the named **NOLOGIN** role. Grant connection to the specified database, schema usage and SELECT on existing and future tables created by the current owner. Do not grant schema creation, ownership or DML. The checker uses `SET ROLE` to test effective permissions; no real password is involved.

```bash
python3 90-tools/practice.py start pg-restore
python3 90-tools/practice.py check pg-restore
```

The check then dumps schema/data, restores into a **different** disposable database, compares rows, rejects a NULL body and inserts a fresh generated ID. Failed inserts may consume IDs; gaps are expected. The dump omits owner/ACL restoration intentionally: role recreation, ACLs and cluster-wide objects require a separate production recovery plan.

## Completion and transfer

Explain creator-specific default privileges and why an owner cannot be made read-only by revoking a table grant. Independently perform a scratch restore, then propose retention, encryption, offsite storage, recovery-point and recovery-time requirements. Do not drop an original database to test whether a backup works.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/pg-restore/explanation.md) · [Backup and restore](https://www.postgresql.org/docs/18/backup.html)
