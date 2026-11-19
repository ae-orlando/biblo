# Capstone lab: read-only inventory

**ID:** `bash-capstone` · **Bash 5+ and GNU find/stat/sort/sed on Linux**, not macOS's default shell/tools.

Prerequisites: Bash track lessons 01–12 and 14–16; complete the four smaller Bash labs first. Outcome: combine quoting, arrays, classification, arithmetic, subprocess status and deterministic output.

## Contract

`bash main.sh [--dry-run] [--top N] [--] DIR`

Recursively inventory regular files without following symlinks. Count files and total bytes by extension. Leading-dot basenames and names without a dot use `none`; other extensions are lowercase ASCII alphanumeric, or `other` if empty/containing other characters.

Output CSV header `extension,count,bytes`, then buckets ordered by count descending and extension byte order ascending. Limit to top N buckets, default 10, permitted range 1..999999. Since bucket names are restricted, records need no arbitrary-filename CSV escaping. Filepaths still require NUL-safe traversal.

Wrong arguments → stderr/`2`; inaccessible directory/traversal failure → nonzero. `--help` succeeds. Dry-run prints a plan without writes; normal execution is also read-only. Totals are bounded by Bash integer capacity; document this limitation.

```bash
python3 90-tools/practice.py start bash-capstone
python3 90-tools/practice.py check bash-capstone
```

Completion: explain every expansion and status boundary, demonstrate a caught bug, then add include/exclude filtering and regression tests. Do not equate a green linter with knowing the entire language.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/bash-capstone/explanation.md) · [Bash manual](https://www.gnu.org/software/bash/manual/)
