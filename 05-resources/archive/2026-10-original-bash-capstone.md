---
created: 2026-10-08
updated: 2026-10-08
---

# Original Bash capstone — historical reference

Archived during the rebuild. The “portable” label and syntax/lint-only mastery claim below are superseded by [[13-bash-capstone]]. Its original two variants are preserved as historical design material.

Build ONE script using everything in notes 01–12 + 14–16. Two variants: **portable** (any Linux/macOS) or **Arch** (this machine). If you can build either clean (`bash -n`, `shellcheck`, no unquoted vars), you know bash as a language.

## Spec A (portable — default)

```
inventory.sh [--dry-run] [--format text|csv] [--top N] [DIR]
```

1. **Args** (note 12): `getopts` `-n/--dry-run`, `--format` (needs value — use GNU `getopt` or `-f` short), `--top N`, optional positional DIR (default `.`). `--help` + exit codes 0/1/2.
2. **Input** (notes 07, 05, 15): `mapfile -t files < <(find "$dir" -type f -print0 | ...)` or NUL-safe `mapfile -d ''`; no pipe-subshell var loss. Prove `while IFS= read -r -d ''` variant in a comment.
3. **Classify** (notes 06, 04, 03): extension via `${f##*.}`, basename via `${f##*/}`, bucket by `case` + `extglob` (`*.{txt,md,sh}` vs `*`).
4. **Count** (notes 02, 05): arithmetic + assoc counts per extension, top-N with `sort | uniq -c | sort -nr | head`.
5. **Output** (notes 09, 11, 15): `text` table or `csv` via `printf '%s,%s\n'`; `--dry-run` prints plan (files touched: none — it only reads, say so). Write report with `> "$out"`, log to stderr.
6. **Robustness** (notes 14, 10, 08): `set -euo pipefail`, `trap` cleanup of temp file, `run()`-style dry mode, functions + `local`, `main "$@"` + source guard, `PS4` trace snippet in comment.

## Spec B (Arch — bonus, this machine)

```
report.sh [--dry-run] [--format text|csv] [--top N] [PKGFILE]
```

1. **Args** (note 12): same flags, optional positional PKGFILE (default: `pacman -Qq` output).
2. **Input** (notes 07, 05): `mapfile -t pkgs` from PKGFILE or `< <(pacman -Qq)`. No pipe-subshell var loss.
3. **Classify** (notes 06, 04): for each pkg, `pacman -Qi` → version via `${line#*: }` strip (no `awk` for this step — prove `${}`), bucket explicit/dependency via `pacman -Qqe` membership in an assoc array.
4. **Count** (notes 02, 05): arithmetic + assoc counts per repo (`pacman -Si` repo field, `${field%% *}`), top-N with `sort | uniq -c | sort -nr | head`.
5. **Output** (notes 09, 11): `text` table or `csv` via `printf '%s,%s\n'`; `--dry-run` prints plan (files touched: none — it only reads, say so). Write report with `> "$out"`, log to stderr.
6. **Robustness** (scripting track): `set -euo pipefail`, `trap` cleanup of temp file, `run()`-style dry mode, functions + `local`, `main "$@"` + source guard.

## Done criteria
- `bash -n report.sh && shellcheck report.sh` clean (zero warnings, not just errors).
- `./report.sh --help` documents itself.
- `./report.sh --dry-run --format csv --top 5` prints plan only, touches nothing.
- Portable: runs on any dir with spaces/newlines in filenames; Arch: `./report.sh --format text --top 10` runs here (hundreds of packages — fast, <5s).
- You can whiteboard the expansion order of its trickiest line from memory.

## After this
You know the language. Next: `03-scripting/` automation patterns + `04-projects/hyprland-installer.md` — same language, destructive context (`--needed`, `stow`, `systemctl`, VM testing).

## Related
- [[00-how-to-use-track|How to Use This Track]]
- [[12-bash-args-options|Args & Options]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]]
- [[15-builtins-printf-read-exec-eval|Builtins]]
- [[90-bash-language-protips|Language Protips]]
