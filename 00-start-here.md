---
type: navigation
updated: 2026-11-19
---

# Start here — learn by producing evidence

This vault is a workshop, not a collection to finish reading. A useful session ends with a working artifact, a test that catches a mistake, or a diagnosis you can defend.

**Your current starting point is no Python knowledge. Start with [[python-learning-path]].** The long-term direction is Python → reliable programs → backend fundamentals → FastAPI → frontend/fullstack integration. Do not start every available track simultaneously; existing project notes do not determine this syllabus.

## Choose your starting point

1. Open [[baseline-diagnostic|Baseline diagnostic]]. Do not infer ability from notes you own.
2. Follow [[master-plan|Learning map]] for prerequisites and project branches.
3. Use [[practice-catalog|Practice catalog]] to choose a lab. Read its specification before its solution.
4. Record only meaningful evidence in [[learning-evidence|Learning evidence]]. Generated content is not completed learning.

| Track | Start | What you will demonstrate |
| --- | --- | --- |
| Python — active first | [[python-learning-path]] | Build, test, debug and maintain useful programs from zero |
| FastAPI — later | [[fastapi-learning-path]] | Validated/tested APIs, dependency boundaries, persistence and ownership policy |
| HTML/CSS — frontend stage | [[html-css-learning-path]] | Semantic forms, accessible native behavior and resilient responsive layouts |
| Git | [[git-learning-path]] | Deliberate staging, history, conflict resolution, review and safe recovery |
| App structure | [[web-app-structure]] | Choose boundaries and growth stages instead of copying one universal tree |
| PostgreSQL | [[postgres-learning-path]] | Defend a schema, query it, handle concurrent writes, inspect plans, restore data |
| JavaScript | [[00-js-how-to-use]] | Validate and transform data, coordinate async work, implement an API and usable client |
| Bash | [[00-how-to-use-track]] | Preserve arguments, design CLIs, handle errors and signals, automate safely |
| Linux | [[linux-learning-path]] | Diagnose permissions, processes and local networking using evidence |
| Engineering support | [[engineering-learning-path]] | Testing, debugging, HTTP/security and transferable delivery habits |

## First concrete session

From a terminal in this directory:

```bash
python3 90-tools/practice.py doctor
python3 90-tools/practice.py list
python3 90-tools/practice.py start py-basics
```

Read [[01-python-execution]] and [[02-python-values]], then [the first Python lab](03-exercises/python-foundations/01-basics/README.md). Edit only `03-exercises/python-foundations/01-basics/work/main.py` for your attempt. Check it:

```bash
python3 90-tools/practice.py check py-basics
```

An unfinished starter should fail. Fix one cause at a time. Then change a requirement and explain the consequences. Do not count a copied reference solution as passing independently.

## Capture and templates

Use one factory so paths and frontmatter stay consistent:

```bash
python3 90-tools/notes.py daily
python3 90-tools/notes.py capture "Idea worth keeping"
note "Idea worth keeping"          # shell helper: create and edit
```

In Neovim, `<leader>mj` opens today's journal, `<leader>mn` captures an inbox
note, and `<leader>mt` creates a concept, project, evidence or review note.
`:VCheck` runs the vault check.

Eight templates live in `99-templates/`: `note`, `concept`, `lab`, `project`,
`daily`, `journal-weekly`, `evidence` and `review`. New material starts in
`00-inbox/`; attachments live in `attachments/`.

## Working rules

- Lab assets and learner code now live **inside this vault**; existing external workspaces are not moved. See [[learning-system]].
- Run commands from the vault root unless a lab says otherwise. Code blocks marked as fragments are not complete programs.
- All bundled automated labs use fake data and local resources. PostgreSQL checks never target your system cluster.
- Browser/manual checklists are separate from automated results.
- Journals, school submissions, channel/creative material, drawings and personal lists remain their own kinds of notes.
- [Implementation and validation status](01-roadmap/implementation-status.md) distinguishes rebuilt material from remaining work.
- [[python-fastapi-expansion-status]] records this Python-first/FastAPI, HTML/CSS, structure and Git expansion. Beginner Python needs no framework/database/browser dependency installation.

## Browse and maintain

[[index|Notes index]] · [[00-journal|Journal]] · [[study-and-review|Study and review]] · [[vault-maintenance|Maintenance and recovery]] · [[obsidian-workflow|Obsidian workflow]]
