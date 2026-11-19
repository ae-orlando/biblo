# Learning map — prerequisites and demonstrated outcomes

Start at [[00-start-here]]. You have stated that you do not know Python: begin with [[python-learning-path]], not a presumed backend bridge. The objective is transferable fullstack engineering with Python/FastAPI, independent of your current project. Use [[baseline-diagnostic]] for other areas; there are no mandatory week counts or parallel-course quota.

## Shared foundation

Read [[learning-system]], then focus on Python. Add small testing/Git habits when you have code to preserve, and HTTP/SQL when approaching backend work. Linux/Bash remain supporting references for actual gaps; they are not another mandatory course to finish before your first Python function.

## Main sequence — one major new subject at a time

1. **Python from zero:** [[python-learning-path]]. Exit: independently implement a validated reporting CLI and changed requirement.
2. **Backend mechanisms:** HTTP, relational modeling/SQL, transactions and safe application access, using the relevant existing database units.
3. **FastAPI:** [[fastapi-learning-path]]. Exit: tested request contracts, dependency boundaries, persistent/concurrent operations and explicit security limits.
4. **Frontend foundations:** [[html-css-learning-path]], then existing JavaScript browser/API work. Framework/TypeScript selection can follow understood platform mechanisms.
5. **Integration and delivery:** an independent fullstack application, end-to-end failures/authorization, documentation, executed deployment/recovery evidence and maintenance under changed requirements.

Use [[git-learning-path]] to preserve/review deliberate changes and [[web-app-structure]] once code needs meaningful boundaries. These support the sequence rather than requiring all topics simultaneously.

## Main learning branches

| Branch | Sequence | Exit evidence |
| --- | --- | --- |
| Databases | [[postgres-learning-path]]: model → query → migrate → contend → measure → recover | Six labs, explained plans, independent schema/change request |
| JavaScript | [[00-js-how-to-use]]: values/functions → data → ESM/CLI → async → HTTP → DOM | Six labs plus [[13-js-capstone]] integration |
| Bash language | [[00-how-to-use-track]]: execution/expansion → structured data/control → I/O → errors/jobs → CLI | Five labs plus [[13-bash-capstone]] change request |
| Linux operations | [[linux-learning-path]]: files/permissions → processes → networking → services | Three automated labs plus an explicitly VM-only incident worksheet |
| Automation | [[30-script-workflow]] after Bash/Linux foundations | Read-only/dry-run evidence, idempotence, failure cleanup, VM evidence before any real installer |

The table is a reference map, not a simultaneous workload. Python is the current active subject; PostgreSQL follows when persistence concepts become relevant. Existing labs remain available without forcing their order from an unrelated project's gaps.

## Optional project references — not the main syllabus

- **Historical/current project material:** [[nies-auth-platform]] and [[30-django-auth-bridge]] remain preserved optional references. Their Django choices, deadlines and inferred starting skills do not determine your Python/FastAPI curriculum.
- **Language integration:** [[13-js-capstone]] extends the tested API/client without pretending the toy API is production-ready authentication.
- **Desktop installer:** [[hyprland-installer]] after Bash/Linux evidence. Keep its eventual real implementation external unless explicitly choosing a vault-local training copy; never modify dotfiles automatically.
- **Database design:** [[universe-database]] becomes an independent design/query exercise, with the original worked example retained as reference.

## Later, when justified by a project

React/TypeScript, Vite, Tailwind, ORM comparisons and containers are follow-on material when useful, not gates before learning Python or the browser platform. Node remains useful in the existing JavaScript track, but Express is not a required second backend. Parked introductions are not represented as complete assessed courses.

## Advancing

Use [[study-and-review]]: behavior, failure cases, explanation, regression test and an unfamiliar change request. Syntax/lint checks are supporting evidence only. Track your own results in [[learning-evidence]].

Historical phase schedules and the previous notes index are retained in `05-resources/archive/`; they no longer define workspace locations or proficiency.
