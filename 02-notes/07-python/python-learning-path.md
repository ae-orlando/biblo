# Python from zero — build competence before a framework

You do not need prior Python knowledge or a current business project. Your immediate subject is **Python**, not Python + FastAPI + React + databases at once. These notes explain the programming prerequisites that the official Python tutorial assumes.

## Start and work independently

From the vault root:

```bash
python3 90-tools/practice.py start py-basics
python3 90-tools/practice.py check py-basics
```

Read [[01-python-execution]] before editing the created work/main.py. An unfinished starter should fail. The first eight labs use only Python's standard library; no pip installation, framework, database or editor plugin is required.

## Sequence and evidence

| Stage | Read | Practice and gate |
| --- | --- | --- |
| Execute and calculate | [[01-python-execution]], [[02-python-values]] | `py-basics`: return correct integer totals, including zero |
| Decide and repeat | [[03-python-control-flow]], basic [[04-python-functions]] | `py-decisions`, `py-loops`: boundary cases and input preservation |
| Functions and data | Full [[04-python-functions]], [[05-python-collections]], [[06-python-errors]] | `py-validation`, `py-records`: explicit failure contracts and independent transformations |
| Real input/output | [[07-python-files]] | `py-files`: real CSV parsing and unchanged output after failure |
| Structure and state | [[08-python-modules]], [[09-python-objects]], [[10-python-tests-types]] | `py-design`: instance isolation and invariant-preserving operations |
| Integrate | [[12-python-capstone]] | `py-cli`: assemble a useful tool, test its process contract, meet a changed requirement |
| Configuration | Relevant errors/modules/testing review | existing `python-config`: explicit settings and safe errors |
| Later async | [[11-python-async]] | Only before the async FastAPI unit, not a first-day requirement |

Use [[practice-catalog]] for exact specifications and separate hints. Follow the table rather than folder numbers: the older python-config path remains stable to preserve links/attempts.

## What progression means

Predict, attempt, read the failure, diagnose, repair, explain and vary the requirement. Documentation and hints are allowed; record assistance honestly. Close a reference solution and rebuild a variant later. Do not award yourself progress because a reference check passes.

Before FastAPI, independently read imperfect CSV, validate records, transform them, write a report safely, explain exceptions and split code into modules. Use [[study-and-review]] and show a regression test catching a deliberate defect.

Then study HTTP/SQL at the point they are needed and follow [[fastapi-learning-path]]. [[git-learning-path]] supports preserving/reviewing work; HTML/CSS is a later focused stage toward fullstack work, not another course to start simultaneously.

References: [version-matched Python 3.14 tutorial](https://docs.python.org/3.14/tutorial/), [library reference](https://docs.python.org/3.14/library/). The official tutorial is aimed at programmers new to Python; these notes add beginner explanations and concrete practice.
