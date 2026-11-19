# Lab: reports that keep missing relationships

**ID:** `pg-queries` · PostgreSQL 15+ · Outcome: get correct results despite zero events, NULL references and tied timestamps.

Prerequisites: [[06-table-joining-methods]], [[08-filtering-sorting-aggregates]], [[12-subqueries-ctes-views]], [[15-window-functions-and-pagination]]. Inspect `fixtures.sql`: four users, five login rows, an anonymous NULL user reference, and a timestamp tie.

## Contract

Define three views in `work/answer.sql`:
- `user_summary(user_id, login_count, last_login)`: every user; count actual matching login rows, not the outer join placeholder. Last login is NULL when absent.
- `never_logged_in(user_id)`: users with no matching login, unaffected by the anonymous row.
- `latest_logins(user_id, login_id, occurred_at)`: one row per user with events. Break timestamp ties with the larger login ID. Exclude the anonymous event.

Initial counts, ordered by user ID: `1→3`, `2→1`, `3→0`, `4→0`. Latest login IDs: `1→14`, `2→12`. The checker changes the data; hard-coded results are not a solution. A view itself promises no output ordering.

```bash
python3 90-tools/practice.py start pg-queries
python3 90-tools/practice.py check pg-queries
```

## Completion and transfer

Explain `COUNT(*)` versus `COUNT(l.id)` after an outer join and why `NOT IN` can fail in the presence of NULL. Extend the report to the latest **successful** login, including users with no successes. Decide where to filter before writing SQL.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/pg-queries/explanation.md) · [Window functions](https://www.postgresql.org/docs/18/tutorial-window.html)
