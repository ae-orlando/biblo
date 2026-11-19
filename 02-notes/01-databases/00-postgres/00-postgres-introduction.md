---
created: 2026-09-26
updated: 2026-10-21
---

# Postgres Introduction

> Start with [[postgres-learning-path]]. Outcome: distinguish a database server, cluster, database, schema, table, role and client, then connect to the intended practice instance. Prerequisite: basic terminal navigation. Practice: the setup step of `pg-schema` in [[practice-catalog]].

**SQL** is a programming language used to manage databases.

PostgreSQL is the database server; `psql` is one client. A **cluster** is an initialized PostgreSQL data directory managed by a server instance and containing multiple databases plus shared objects such as roles. A **database** contains schemas, which contain tables and other objects. A connection chooses one database and role. The shell's current directory does not choose the database.

In Postgres, data is stored in related tables.

## Postgres

- An object-relational DBMS.

## CLI, Terminal & Shell

- **CLI:** A program interface that takes text commands (e.g. `psql`).
- **Terminal:** The app that shows the text window (e.g. GNOME Terminal, Alacritty).
- **Shell:** The command interpreter running inside the terminal (e.g. `bash`, `zsh`) that parses and executes your input.

## Relational Databases

- Store data in tables.
- Link different pieces of information by joining tables through common attributes.

## Query

A query is a request for specific information from a database.

## NoSQL (Non-Relational Databases)

An umbrella term for non-relational data models such as documents, key-value stores and graphs. Capabilities vary: some support joins, schemas and transactions. “NoSQL” does not mean “no relationships” or automatically more flexible/better.

## Installation (Arch)

**Host-administration reference, not the course setup.** Do not run these commands on an existing cluster to do the labs. The bundled helper initializes a separate vault-local cluster without sudo or changing a system service.

```shell
sudo pacman -S postgresql
```

Optional GUI for viewing databases:

```shell
yay -S pgadmin4-desktop-bin
yay -S pgadmin4-server-bin
```

> Install only `-desktop-bin` for local GUI use. Skip `-server-bin` unless you need to run pgAdmin as a web server.

## Initial Setup

```shell
sudo su -l postgres -c "initdb --locale=C.UTF-8 --encoding=UTF8 '/var/lib/postgres/data'"
```

This initializes the database cluster and sets character encoding.

Never initialize over an existing data directory. Host package/service installation requires a separate deliberate administration decision; the lab checker does not perform it.

## Check and retrieval

Run `python3 90-tools/practice.py doctor`, then `python3 90-tools/postgres.py start`. Open `python3 90-tools/postgres.py psql` and inspect `\conninfo`, `SELECT current_database(), current_user;`, and `SHOW data_directory;`. Confirm the vault-local directory before any write. Stop with `python3 90-tools/postgres.py stop` when finished.

Explain why installing psql alone does not create an application database, and why two servers can both contain a database named `postgres` without being the same instance.

Sources: [Architectural fundamentals](https://www.postgresql.org/docs/18/tutorial-arch.html), [database cluster creation](https://www.postgresql.org/docs/18/creating-cluster.html).

## Related Notes

- [[01-psql-workflow|psql Workflow]]
- [[02-sql-datatypes|SQL Datatypes]]
- [[03-inserting-and-viewing-data|Inserting and Viewing Data]]
- [[04-primary-foreign-keys|Primary & Foreign Keys]]
- [[05-relationships|Relationships]]
- [[06-table-joining-methods|Table Joining Methods]]
- [[07-updating-and-deleting-data|Updating and Deleting Data]]
- [[08-filtering-sorting-aggregates|Filtering, Sorting & Aggregates]]
- [[09-altering-tables|Altering Tables]]
- [[10-transactions|Transactions]]
- [[11-indexes-and-performance|Indexes & Performance]]
- [[12-subqueries-ctes-views|Subqueries, CTEs & Views]]
- [[13-admin-and-ops|Admin & Ops]]
