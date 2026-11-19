---
type: navigation
updated: 2026-11-19
---

# Journal

Raw experience lives here. Durable lessons get promoted out of the journal; the journal itself stays dated and honest.

## Cadence

| Note | Location | Template | When |
| --- | --- | --- | --- |
| Daily | `06-journal/YYYY/YYYY-MM-DD-dddd.md` e.g. `2026-11-18-Wednesday.md` | [[daily]] | End of a session, or the same evening |
| Weekly | `06-journal/YYYY/YYYY-Www.md` e.g. `2026-W47.md` (week 47 of 2026) | [[journal-weekly]] | Last session of the week |

The core Daily Notes plugin creates the daily note in the current year folder. Create the weekly note manually in the same year folder and insert [[journal-weekly]] with Templates.

From Neovim, `:Journal` and `:Weekly` (equivalently `python3 90-tools/notes.py daily|weekly`) apply the same templates immediately; `:Journal` does not depend on the Obsidian plugin. Existing notes are opened, never overwritten.

## Rules

- One daily note per day. Append; don't rewrite. A wrong hypothesis stays visible next to the correction that replaced it.
- Record artifact paths and actual check output, not intentions.
- Keep it short. If an entry takes longer than the session, it is turning into an essay — promote the durable part.
- Personal reflection is fine; secrets, credentials and private third-party data are not.
- Promote repeated tricks to `02-notes/*/90-*-protips.md` and durable assessment evidence to [[learning-evidence]].

## What belongs elsewhere

- Concept or reusable reference → `02-notes/`
- Lab spec or attempt → `03-exercises/`
- Project requirements → `04-projects/`
- External material → `05-resources/`
- Reference solution → `07-solutions/`

## Current

- This week: [[2026-W47]]
- Current year folder: `06-journal/2026/`
