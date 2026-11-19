# Baseline diagnostic — choose evidence, not labels

**Current placement:** you explicitly have no Python knowledge. Start [[python-learning-path]] at execution/values and py-basics; the advanced configuration task below is a later checkpoint, not an entry requirement. Use other rows only when deciding which existing skills need a bridge.

Use this before choosing a branch. Existing notes alternately describe a first-time programmer and an experienced JavaScript user; neither is a current assessment. Do not tick anything merely because it feels familiar.

Try the task first, then consult documentation and explain what it changed. These are diagnostic observations, not graded exams or prerequisites to opening a lesson.

| Area | Independent task | Evidence and routing |
| --- | --- | --- |
| Shell | Pass a filename containing spaces and a newline as one argument; distinguish stdout, stderr and status | If unclear: [[01-shell-model]], [[03-quoting-splitting-globbing]], then `bash-quoting` |
| Linux | Explain a permissions failure using parent-directory access and file mode; distinguish a missing process from a denied operation | [[linux-learning-path]] and `linux-permissions` / `linux-processes` |
| JS fundamentals | Parse user-entered counts without accepting blanks, suffixes or unsafe integers | `js-values`; bridge through values, functions and errors if needed |
| JS data | Group records without mutating input, including duplicate IDs and a `__proto__` user | `js-data`; review objects/arrays before proceeding |
| Async | Explain why a slower old request must not replace a newer result | `js-async`; do not use timer speed as the only proof |
| SQL | Design users/profiles/login events, defend keys, then deliberately violate constraints | `pg-schema`; missing explanation → database foundations |
| SQL querying | Include users with zero events and choose the latest event deterministically | `pg-queries`; missing rows → joins, NULLs and grouping |
| Reliability | Show failed writes preserve invariants and recover a backup into a different database | `pg-transfer`, `pg-restore`; reading commands alone is insufficient |
| Python later checkpoint | Validate an explicit configuration mapping without leaking a token in errors | `python-config` after core [[python-learning-path]] units; then the FastAPI entry gate |

## Record the result

For each attempted area: artifact path, check output, what needed help, one explanation, and the next bridge. Use [[learning-evidence]]. Leave unattempted areas unassessed.

Skip introductory reading only if you can complete an independent task **and** explain the mechanism and a failure case. Do not skip cumulative checkpoints or security/operational boundaries based on confidence alone.
