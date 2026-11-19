# Learning system — conventions and boundaries

## One source of truth for each kind of material

| Location | Purpose |
| --- | --- |
| `00-start-here.md` | Entry point |
| `01-roadmap/` | Sequence, diagnostics, assessment, progress and maintenance |
| `02-notes/` | Concepts and reusable reference |
| `03-exercises/<track>/<lab>/` | Specifications, starter files, checks, fixtures, hints and learner `work/` |
| `04-projects/` | Requirements and capstones; project implementation locations are explicit |
| `05-resources/` | Supporting resources and historical plans |
| `06-journal/` | Daily logs in year folders and weekly reviews; dated experience, error analysis and evidence |
| `07-solutions/<lab-id>/` | Reference code and explanations; read after attempting |
| `90-tools/` | Authored launchers and validators |
| `99-templates/` | Templates for different note types |
| `.practice-runtime/` | Disposable test artifacts and the isolated PostgreSQL cluster |
| `.tools/` | Optional vault-local tool installations |
| `.vault-backups/` | Recovery snapshots, outside normal note navigation |

`~/learning/` and `~/dotfiles/` are external, existing workspaces, not prerequisites for these labs. Older instructions that put new course exercises there are superseded. Never copy a whole external project into the vault automatically; keep real deployment work separate and link its location explicitly.

## Session loop

Predict → study a small section → attempt → check → diagnose → repair → explain → vary the requirement → record evidence. Documentation is allowed during engineering tasks. Brief closed-note retrieval checks mental models, not API trivia.

The launcher copies `starter/` into `work/` only when `work/` does not exist. It never resets an attempt. To retry, preserve your work under a distinct name yourself, then start again. There is deliberately no destructive reset command.

## Lesson, drill, lab and project

- A **lesson** explains a mechanism and links to practice.
- A **scratch drill** is a small program you author yourself inside a related lab's `work/`. Old suggested filenames are ideas, not distributed assets.
- A **lab** has a concrete contract and checkable behavior. Its specification outranks a historical scratch-drill gate.
- A **project** integrates skills with design freedom; use a rubric and independent change request, not only tests.

Lab IDs are stable and registered in `90-tools/labs.json`. Keep them independent of lesson numbering: one lab can exercise several lessons. Retain useful concept slugs; use qualified wikilinks or relative Markdown links for repeated filenames such as `README.md`.

## Safety and assessment

No host package installation, sudo, external credentials, remote services, live database changes, Git initialization or publication is performed by the launcher. Do not run historical administration examples on your host merely because they appear in a note. VM-only work is explicitly labeled.

Tests execute your code with your user permissions; they are **not a security sandbox**. Inspect unfamiliar code. The database helper restricts its own connections, not what arbitrary learner code could do.

Reference checks show the supplied solution meets tested cases. They do not show that you have mastered the topic. Retained historical examples are reviewed selectively; only executions listed in the validation record count as reverified.
