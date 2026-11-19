---
created: 2026-09-26
updated: 2026-10-21
---

# psql Workflow

> Prerequisite: [[00-postgres-introduction]]. Outcome: prove which instance/database/role a command will affect and distinguish object ownership from granted access. Practice: `pg-schema` and `pg-restore` in [[practice-catalog]].

## Safe course entry point

```bash
python3 90-tools/postgres.py start
python3 90-tools/postgres.py psql
```

Use `\conninfo` and `SHOW data_directory;` before writes. This helper ignores inherited PG connection settings and chooses the private practice socket explicitly. An ordinary bare `psql` command may connect elsewhere.

Postgres creates a default superuser called `postgres`. Use it for admin only — never for applications.

## Per-Project Workflow

The following is **administration reference**, not an instruction to modify your system cluster. In the isolated course cluster, the administrator is `vault_admin`, not `postgres`. An owner role is suitable for schema/migration work; a least-privilege runtime app role should not own those objects.

For each new project, create a dedicated user + database:

1. Log in as the `postgres` superuser:

```bash
sudo -u postgres psql
```

2. Then in `psql`:

```sql
CREATE USER new_user_name;
\password new_user_name
CREATE DATABASE new_database_name OWNER new_user_name;
```

On a newly created PostgreSQL 15+ database, the database owner ordinarily has access to create objects in public through `pg_database_owner`. Extra blanket grants to that same owner are not generally necessary. Inspect effective ownership and privileges instead of pasting grants until an error disappears.

```sql
\c new_database_name
\dn+
\dp
```

3. Log in as the new user:

```bash
psql -U <username> -d <database_name> -h localhost
```

- `-h localhost` chooses TCP; the matching pg_hba.conf rule determines authentication. It does not inherently force password authentication. Unix sockets can use peer, password or other configured methods too.
- Connection string form (apps / `.env`): `postgres://<username>:<password>@localhost:5432/<database_name>`

## Essential psql Commands

| Command | What it does |
|---|---|
| `\l` | List databases |
| `\c <db>` | Switch database |
| `\dt` | List tables |
| `\d <table>` | Describe table |
| `\du` | List users/roles |
| `\q` | Quit |

## Quick-Test Shortcut (Superuser Only)

If you don't want to create another user yet, create a database then switch to it in the `psql` shell:

```psql
\c database_name
```

The prompt changes to the database name. See [[02-sql-datatypes|SQL Datatypes]] for column types and [[03-inserting-and-viewing-data|Inserting and Viewing Data]] for a full `CREATE TABLE` + `INSERT` + `SELECT` example.

## Check and retrieval

In `pg-restore`, explain why connecting to a database, resolving a schema and reading a table require different permissions. Check failures as well as successful SELECTs. A password entered through `\password` avoids embedding a literal in SQL history, but credentials still require appropriate storage and transport policies.

Sources: [psql](https://www.postgresql.org/docs/18/app-psql.html), [schemas](https://www.postgresql.org/docs/18/ddl-schemas.html), [client authentication](https://www.postgresql.org/docs/18/client-authentication.html).

## Related Notes

- [[00-postgres-introduction|Postgres Introduction]]
- [[13-admin-and-ops|Admin & Ops]]
- [[03-inserting-and-viewing-data|Inserting and Viewing Data]]
