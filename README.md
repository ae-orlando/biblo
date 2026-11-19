# Notes Vault — Automata Theory & Lucky

Welcome to the **Notes Vault** repository. This collection captures daily notes, insights, and quick thoughts organized by date. It uses a simple markdown capture workflow via the `00-inbox/` directory, which can be rapidly committed to the vault.

## What We Made

- **Two capture notes** added on 2026‑11‑19:
  - `00-inbox/2026-11-19-automata-theory-19th.md` — a structured automata‑theory note (Thought / Why it matters / Next actions).
  - `00-inbox/2026-11-19-lucky.md` — a personal note about "Lucky", including a thought, why it matters, and next actions with a signature "Orlando" tag.

Both notes follow the same front‑matter convention (`type: capture`, `created: "YYYY-MM-DD"`) and a consistent outline (Thought, Why it matters, Next), making them easy to search, link, and transform with tooling like **matugen** or **Hyprland**‑oriented workflows.

## Features Implemented

| Feature | Description |
|---|---|
| **Capture workflow** | Drop markdown files into `00-inbox/` with a date‑prefixed filename. The `git add 00-inbox/ && git commit -m "docs(vault): capture notes for <date>"` command (or a custom script) pushes them into the vault. |
| **Front‑matter metadata** | Each note starts with a YAML‑style block (`type`, `created`). This enables programmatic filtering, tagging, and rendering in vaults that understand front‑matter. |
| **Standard outline** | Every note includes `Thought`, `Why it matters`, and `Next` sections. The `Next` section uses checkboxes (`- [ ]`) that can be toggled off as items are completed. |
| **Consistent naming** | Files are named `YYYY-MM-DD‑slug.md`, making chronological sorting trivial and providing a clear semantic meaning. |
| **Provenance tracking** | Git history records who added each note and when, via standard commits. The commit message follows the `docs(vault): …` convention for easy `git log` queries. |
| **Ease of extension** | New notes can be added manually or via a small wrapper script that auto‑generates the front‑matter and empty sections. |

## How to Use

1. **Add a new note**
   - Create a file in `00-inbox/` named `YYYY-MM-DD‑<topic>.md`.
   - Use the following template (copy‑paste and fill in):

   ```markdown
   ---
   type: capture
   created: "YYYY-MM-DD"
   ---

   # <title>

   ## Thought

   ## Why it matters

   ## Next
   - [ ]
   ```

   - Example (the two notes already committed):

   ```markdown
   ---
   type: capture
   created: "2026-11-19"
   ---

   # automata-theory-19th

   ## Thought

   ## Why it matters

   ## Next
   - [ ]
   ```

2. **Commit the note to the vault**
   ```bash
   git add 00-inbox/
   git commit -m "docs(vault): capture notes for 2026-11-19"
   git push   # if you have a remote
   ```

3. **Search / filter notes**
   - Use `grep` or your favorite markdown search tool on the `type: capture` front‑matter or on the `created` date.
   - Example: `grep -R "type: capture" 00-inbox/` lists all capture notes.

4. **Toggle “Next” actions**
   - The `## Next` section contains checkboxes. Mark them `- [x]` when done, or add new ones as actions arise.

## Pro Tips & Best Practices

- **Batch‑commit daily**: At the end of each day, run `git add 00-inbox/ && git commit -m "docs(vault): capture notes for $(date +%F)"` to keep the history tidy.
- **Link notes across dates**: Because notes are dated, you can reference another note in `Why it matters` or `Next` using relative markdown links, e.g., `[see 2026-11-18]($`../../2026-11-18-something.md``.
- **Tag with topics**: Add a `#automata-theory` or `#lucky` hashtag inside the `## Thought` or `## Why it matters` sections for full‑text searchability.
- **Automate with a script**: Write a tiny shell wrapper that takes a title, generates the filename from today's date, populates the front‑matter, and opens the file in your editor:
  ```bash
  #!/usr/bin/env bash
  DATE=$(date +%F)
  SLUG=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  FILE="00-inbox/${DATE}-${SLUG}.md"
  cat > "$FILE" <<EOF
  ---
  type: capture
  created: "$DATE"
  ---

  # $1

  ## Thought

  ## Why it matters

  ## Next
  - [ ]
  EOF
  ${EDITOR:-nvim} "$FILE"
  ```
  Save it as `add-note.sh`, make it executable, and run `./add-note "My new thought"`.
- **Integrate with tooling**: The front‑matter `type: capture` can be consumed by vault‑aware tools (e.g., Obsidian plugins, custom scripts) to surface recent captures, generate dashboards, or sync with other systems.
- **Keep the inbox clean**: After committing, you can delete the processed files from `00-inbox/` if you prefer an ephemeral inbox, or leave them as a permanent archive.

## Quick Reference Commands

```bash
# List all capture notes
grep -l "type: capture" 00-inbox/*.md

# Show recent commits about vault notes
git log --oneline --all -- 00-inbox/

# Add & commit today's note
git add 00-inbox/
git commit -m "docs(vault): capture notes for $(date +%F)"
git push origin main
```

---

*Happy note‑taking! May your automata be orderly and your luck ever in your favor.*