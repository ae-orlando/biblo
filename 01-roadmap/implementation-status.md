# Rebuild status and verification record

Started 2026-10-20; continued 2026-10-21. This records authored material and **reference** verification, not learner completion.

**This page records the first rebuild's 21-lab baseline.** The clarified Python-from-zero/FastAPI direction and added HTML/CSS, app-structure and Git material are tracked in [[python-fastapi-expansion-status]]. Current entry: [[python-learning-path]], not the older pg-schema recommendation preserved below as history.

## Implemented

- Verified pre-change snapshot: `.vault-backups/pre-learning-rebuild-20261020T202810Z.tar.gz`, with SHA-256 manifest and 127 regular files compared against archive contents.
- A vault entry point, learning map, diagnostics, evidence/review workflow and differentiated templates.
- 21 executable lab packages: PostgreSQL 6, JavaScript 6, Bash 5, Linux 3, Python bridge 1. Each includes a specification, unfinished starter, checks, hints and a separate explained reference.
- Vault-local launcher with non-overwriting workspace creation, deterministic fixtures and a private PostgreSQL cluster.
- Core lesson corrections and explicit links to behavioral practice; additional schema/NULL, windows/pagination, concurrency, browser and engineering bridges.
- ShellCheck 0.11.0 installed only at `.tools/bin/shellcheck`, from the official upstream Linux x86_64 asset after comparing its SHA-256 with the release metadata. No system package/global PATH changes.

## Executed verification — 2026-10-21

All **21 reference lab suites passed**, all **21 unfinished starters failed as expected**, and the tests caught **9 representative mutations**. These are 51 successful audit expectations, not 51 learner exercises completed. Full results/logs are under `.practice-runtime/validation/`, including `results.json` with the actual UTC execution timestamp.

PostgreSQL checks exercised constraints, changed data, atomic migration failure, concurrent transfers, index/query behavior and a separate restore. Node/Bash/Python checks exercised their packaged contracts. Boundary review added an empty-inventory test and explicit rejection of port zero. The restore check allows sequence gaps after a failed insert rather than assuming gapless identity values.

`check-vault.py --code` passed local file-link/fence checks, lab completeness, Obsidian JSON parsing, standalone Python/Node/Bash syntax checks and ShellCheck. It does not check every external URL or execute historical Markdown snippets. `check-tooling.py` passed **6 smoke tests**, including non-overwriting workspace creation, inherited-PG-setting isolation, the coherent SQL demo, selected corrected Bash/ESM semantics and restricted local web fixture serving.

`verify-backup.py` reverified the archive digest and **127 original regular-file hashes**. A separate baseline comparison confirmed **44 protected original files unchanged**, covering personal/root material, journals, schoolwork, channel/creative files, drawings/attachments and installed community-plugin files. Existing personal history was not replaced with generated learning achievements.

Runtime context: Node 24.21.0, Bash 5.3.20, PostgreSQL 18.6, Python 3.14.8, vault-local ShellCheck 0.11.0. The practice cluster is stopped at handoff; the launcher starts it again when needed.

## Manual or unverified boundaries

- DOM rendering, keyboard/assistive-technology behavior and the required browser checklist.
- Learner plan interpretation and independent capstone/change requests.
- VM/service/package administration, real deployments, Git learner repository tasks and Django application builds.
- Obsidian UI reload/render behavior; configuration/files on disk are distinguishable from observed UI behavior.
- Retained historical command catalogs and archived schedules are not all re-executed or current environment inventories.
- School/personal/channel/creative material is preserved, not substantively assessed as a technical curriculum. Parked Vite/Tailwind/Docker introductions are not complete assessed tracks.

## Handoff and remaining work

The core learning-system rebuild is delivered. Open [[00-start-here]], run the baseline diagnostic and attempt `pg-schema` (or the diagnostic-selected bridge). Reload Obsidian if needed for the new daily-note folder/template settings. No additional community plugin was necessary; existing plugin installations were preserved.

Further work is evidence-driven: complete manual browser/plan/VM/project checks, expand tests when an uncovered behavior appears, and develop later framework/tooling tracks only when a real project needs them. Historical version catalogs, personal/school/channel content and parked introductions are not represented as comprehensively verified courses.
