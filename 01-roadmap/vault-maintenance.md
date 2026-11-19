# Vault maintenance, validation and recovery

## Run from the vault root

These are author/maintenance audits, not prerequisites to the first Python exercise. The full suite includes FastAPI and real-browser labs and therefore needs their marked local environments; see `90-tools/README.md`. To practise just beginner Python, start/check py-basics and follow [[python-learning-path]].

```bash
python3 90-tools/practice.py doctor
python3 90-tools/check-vault.py --code
python3 90-tools/check-tooling.py
python3 90-tools/audit-practice.py
python3 90-tools/verify-backup.py
```

The practice audit runs **reference** checks, confirms unfinished starters fail, and injects representative bugs into disposable copies to test the tests. It does not initialize learner workspaces or award learning progress. Results and full logs live in `.practice-runtime/validation/`; [[implementation-status]] summarizes actual executions and limits.

The tooling smoke test uses an isolated temporary mini-vault to prove that starting again preserves a learner's edits. Its printed test workspace is deleted with that fixture; no real learner workspace is created. Its web checks verify HTTP assets/API boundaries, not rendered browser behavior.

The link checker excludes hidden runtime/tools/backups and learner work. It checks local file links, code fences, lab assets, Obsidian JSON and optional standalone syntax/shell lint. It does not itself validate every external URL, block ID, browser behavior or plugin UI. Real-browser exercises have separate executable checks; a clean static report is not an accuracy certificate for all historical prose.

## Database lifecycle

```bash
python3 90-tools/postgres.py start
python3 90-tools/postgres.py status
python3 90-tools/postgres.py psql
python3 90-tools/postgres.py stop
```

The helper manages only `.practice-runtime/postgres/`, with a private Unix socket and no TCP listener. It refuses an unmarked or escaping/symlinked runtime path and specifies connection arguments rather than inheriting PGHOST/PGDATABASE. Tests use fake data and uniquely named disposable databases; no system service is changed.

Stop it after practice. There is intentionally no blanket reset/delete command. Preserve any learner-created scratch database you want before choosing to rebuild disposable runtime data. Never “clean up” by deleting a guessed /var/lib/postgres path or connecting to the default socket.

## Recover original content

The pre-change snapshot and its manifest are in `.vault-backups/`. `verify-backup.py` compares archive bytes and archived regular-file hashes with the recorded baseline; it does not compare rewritten current notes or restore anything.

The later Python/FastAPI expansion has its own verified snapshot, excluding regenerable runtime data. Verify it explicitly with:

```bash
python3 90-tools/verify-backup.py .vault-backups/pre-python-fastapi-expansion-20261021T095055Z.tar.gz
```

For recovery, extract into a **new empty review directory inside this vault's backup area**, inspect the selected files, then restore only the intended content after preserving newer work. Do not unpack blindly over the live vault or replace all .obsidian settings while Obsidian is writing them. The snapshot includes original configuration and attachments, not an external/offsite backup guarantee.

## Migration record

| Original | Preserved historical location / treatment |
| --- | --- |
| `01-roadmap/master-plan.md` | `05-resources/archive/2026-10-original-master-plan.md`; new learning map keeps the original link target |
| `02-notes/index.md` | `05-resources/archive/2026-10-original-notes-index.md`; new notes index keeps the original link target |
| JS `00-js-how-to-use.md` | `05-resources/archive/2026-10-original-js-track-guide.md`; replaced at the original path |
| JS `13-js-capstone.md` | `05-resources/archive/2026-10-original-js-capstone.md`; consistent new capstone at original path |
| Bash `00-how-to-use-track.md` | `05-resources/archive/2026-10-original-bash-track-guide.md`; replaced at original path |
| Bash `13-bash-capstone.md` | `05-resources/archive/2026-10-original-bash-capstone.md`; GNU/Linux contract at original path |
| Misplaced journal fragment in JS values note | `06-journal/2026/2026-10-08-imported-js-fragment.md` (currently absent from the vault); original bytes also in snapshot |
| `04-projects/universe-database.md` worked script | `05-resources/archive/2026-10-universe-worked-example.md`; independent project brief at original path, original learner design preserved separately |

Other educational corrections are in place, with original versions recoverable from the snapshot. Personal lists, journal entries, school submissions, channel material, drawings and image attachments are not silently replaced with curriculum text. Any further migrations are added here explicitly.

The Python/FastAPI expansion updates navigation in place to remove current-project/Django assumptions; it adds new course/lab directories without moving learner attempts. The pre-expansion snapshot preserves the preceding roadmap. Git exercises remain explicit learner actions: no repo/commit/global identity/remote was created by the author.

## Maintenance rules

- Check the registry and links after changing a lab ID/path or concept slug.
- Keep full solutions separate; never overwrite a learner's work/.
- Re-run relevant positive, negative and regression cases after changing a contract.
- Update sources and runtime context when behavior depends on versions; distinguish reviewed from executed.
- Treat Git/project setup, privileged commands, deployments and remote integrations as separately scoped actions, not automatic maintenance.
- Keep real secrets out of examples, evidence logs, screenshots, backups intended for sharing and published repositories.

Implementation entry points: `90-tools/practice.py:1`, `90-tools/postgres.py:1`, `90-tools/check-vault.py:1`, `90-tools/audit-practice.py:1`, `90-tools/verify-backup.py:1`.
