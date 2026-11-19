# Lab: index a query using evidence

**ID:** `pg-plans` · Outcome: explain a query plan and the cost of an index, not celebrate every index scan.

Prerequisites: [[11-indexes-and-performance]], [[15-window-functions-and-pagination]]. `fixtures.sql` creates 30,000 deterministic events.

## Contract

Add `events_recent_login`, a B-tree index on `(user_id, created_at DESC, id DESC)` containing only rows whose `kind = 'login'`. Do not change fixture data or planner settings.

Target query: recent login event IDs for one user, ordered by timestamp and ID descending, limited to five. Tests check the index definition, unchanged results and an executed JSON plan. They deliberately do **not** require one particular optimizer node or speedup.

```bash
python3 90-tools/practice.py start pg-plans
python3 90-tools/practice.py check pg-plans
```

## Required manual investigation

Open `python3 90-tools/postgres.py psql`, create your own `learner_plans` database, connect to it, then load the fixture with `\i 03-exercises/postgres/05-plans/fixtures.sql`. Capture `EXPLAIN (ANALYZE, BUFFERS)` before and after loading your `work/answer.sql`.

Compare a selective user query with a query returning most rows. Explain estimates versus actual rows, loops, buffers, sort work and write/storage overhead. An index-only scan can still fetch heap pages. Save the plans and interpretation in your `work/` directory. Drop only the learner database you created when finished.

Completion requires this interpretation, not just the automated check. Extend to keyset pagination and defend the index order.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/pg-plans/explanation.md) · [Using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html)
