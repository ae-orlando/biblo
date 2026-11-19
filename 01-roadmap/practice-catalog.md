# Practice catalog

Run `python3 90-tools/practice.py list` for the executable registry. All commands below run from the vault root:

```bash
python3 90-tools/practice.py start LAB-ID
python3 90-tools/practice.py check LAB-ID
```

Replace `LAB-ID`, do not type it literally. `start` preserves an existing `work/` directory by refusing to overwrite it. `check` does not read solutions. `--reference` is for auditing the supplied solution, not earning completion credit.

## Python from zero — current first track

| ID | Specification | Prerequisites / outcome |
| --- | --- | --- |
| `py-basics` | [First function](../03-exercises/python-foundations/01-basics/README.md) | First execution/values lessons; integer totals |
| `py-decisions` | [Decisions](../03-exercises/python-foundations/02-decisions/README.md) | Conditions and threshold boundaries |
| `py-loops` | [Loops](../03-exercises/python-foundations/03-loops/README.md) | Sequences and accumulators without mutation |
| `py-validation` | [Validation](../03-exercises/python-foundations/04-validation/README.md) | Functions/errors; explicit type/syntax/range |
| `py-records` | [Records](../03-exercises/python-foundations/05-records/README.md) | Collections/errors; independent aggregation |
| `py-files` | [Files](../03-exercises/python-foundations/06-files/README.md) | CSV parsing and safe output |
| `py-design` | [State and objects](../03-exercises/python-foundations/07-design/README.md) | Invariants and instance isolation |
| `py-cli` | [Reporting CLI](../03-exercises/python-foundations/08-cli/README.md) | Independent assembly and failure contract |

Follow [[python-learning-path]], not every table at once. Beginner Python uses only the standard library.

## FastAPI — later, after prerequisites

| ID | Specification | Evidence |
| --- | --- | --- |
| `api-contract` | [HTTP contract](../03-exercises/fastapi/01-contract/README.md) | Validation, statuses, output and OpenAPI |
| `api-dependencies` | [Dependencies](../03-exercises/fastapi/02-dependencies/README.md) | App isolation and substituted boundary |
| `api-async` | [Async work](../03-exercises/fastapi/03-async/README.md) | Bounded concurrency/deadline/cleanup |
| `api-postgres` | [Persistence](../03-exercises/fastapi/04-postgres/README.md) | Real database and competing reservations |
| `api-ownership` | [Ownership](../03-exercises/fastapi/05-ownership/README.md) | Default denial and object policy; real authentication remains separate |

## HTML/CSS — focused frontend foundations stage

`web-html`: [Semantic form](../03-exercises/html-css/01-html/README.md). `web-css`: [Responsive layout](../03-exercises/html-css/02-css/README.md). Both use actual Chromium plus required manual judgment; see [[html-css-learning-path]].

Git has a [manual local workflow](../03-exercises/git/01-local-workflow/README.md) and an optional read-only artifact checker; it is not a silently executed repo/commit operation or part of the automatic reference-suite count. Structure practice is in [[03-boundaries-and-refactoring]].

## PostgreSQL

| ID | Specification | Builds on |
| --- | --- | --- |
| `pg-schema` | [Schema and constraints](../03-exercises/postgres/01-schema/README.md) | Types, keys, cardinality, NULL |
| `pg-queries` | [Reports and latest rows](../03-exercises/postgres/02-queries/README.md) | Joins, aggregates, subqueries, windows |
| `pg-migration` | [Atomic backfill](../03-exercises/postgres/03-migration/README.md) | Updates, constraints, transactions |
| `pg-transfer` | [Concurrent transfers](../03-exercises/postgres/04-transfer/README.md) | Transactions, locks, invariants |
| `pg-plans` | [Measured indexing](../03-exercises/postgres/05-plans/README.md) | Query plans; manual interpretation required |
| `pg-restore` | [Permissions and recovery](../03-exercises/postgres/06-restore/README.md) | Roles, dumps, restore verification |

## JavaScript

| ID | Specification | Builds on |
| --- | --- | --- |
| `js-values` | [Count parsing](../03-exercises/js-lang/01-values/README.md) | Values, control flow, functions, strings, errors |
| `js-data` | [Pure aggregation](../03-exercises/js-lang/02-data/README.md) | Objects, arrays, Map/Set, validation |
| `js-cli` | [File-report CLI](../03-exercises/js-lang/03-cli/README.md) | ESM, Node filesystem, errors |
| `js-async` | [Concurrency and stale results](../03-exercises/js-lang/04-async/README.md) | Closures, promises, async/await |
| `js-http` | [Todo API](../03-exercises/js-lang/05-http/README.md) | HTTP, streams, async errors, testing |
| `js-dom` | [Accessible local client](../03-exercises/js-lang/06-dom/README.md) | DOM, fetch, UI state; browser checklist required |

## Bash and Linux

| ID | Specification |
| --- | --- |
| `bash-quoting` | [Arbitrary filenames](../03-exercises/bash-lang/01-quoting/README.md) |
| `bash-cli` | [Safe CLI and output replacement](../03-exercises/bash-lang/02-cli/README.md) |
| `bash-pipeline` | [Validated log summary](../03-exercises/bash-lang/03-pipeline/README.md) |
| `bash-jobs` | [Worker lifecycle](../03-exercises/bash-lang/04-jobs/README.md) |
| `bash-capstone` | [Read-only inventory](../03-exercises/bash-lang/05-capstone/README.md) |
| `linux-permissions` | [Marked permissions sandbox](../03-exercises/linux/01-permissions/README.md) |
| `linux-processes` | [Non-destructive process inspection](../03-exercises/linux/02-processes/README.md) |
| `linux-network` | [Layered HTTP diagnosis](../03-exercises/linux/03-network/README.md) |

## Configuration — after core Python

`python-config`: [Explicit configuration validation](../03-exercises/python/01-config/README.md).

## What a green check means

The checked implementation passed the bundled cases. You still need to explain it, introduce and detect a bug, and handle a changed requirement. Browser behavior, plan interpretation, VM administration and production readiness require additional evidence. See [[study-and-review]].
