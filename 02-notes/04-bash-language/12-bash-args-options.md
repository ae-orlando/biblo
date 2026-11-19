---
created: 2026-10-08
updated: 2026-10-21
---

# 12 — Args and Options (`$@`, `getopts`, CLI design)

> Prerequisites: arrays, conditionals and functions. Outcome: test an argument grammar including missing values, unknown flags and --. Practice: `bash-cli` in [[practice-catalog]]. Its reference uses an explicit case loop without eval.

## Mental model

Script interface: positionals (`$1`, `$@`) for targets, flags for behavior. `getopts` parses short opts (`-y`, `-n`); `--long` needs the `-:` extension or GNU `getopt`. Always `shift $((OPTIND - 1))` after parsing so `"$@"` holds only positionals. Verified parsing demo in Try it.

```bash
install() { local pkg="$1"; echo "pkg=$pkg"; }  # functions have their OWN $@
```

## `getopts` with `--long` support (verified pattern)
```bash
DRY_RUN=0; YES=0
while getopts ":yn-:" opt; do
  case "$opt" in
    -) case "$OPTARG" in
         dry-run) DRY_RUN=1 ;;
         yes) YES=1 ;;
         format=*) FORMAT="${OPTARG#*=}" ;;  # --format=csv style (manual split)
         *) echo "unknown --$OPTARG" >&2; exit 2 ;;
       esac ;;
    y) YES=1 ;;
    n) DRY_RUN=1 ;;
    :) echo "missing arg -$OPTARG" >&2; exit 2 ;;
    \?) echo "bad -$OPTARG" >&2; exit 2 ;;
  esac
done
shift $((OPTIND - 1))   # "$@" now = positionals only
# -- ends options; Bash getopts stops at the first non-option argument.
```
`:` prefix = silent errors (you handle `:`/`?`). `OPTIND` starts at 1 — reset `OPTIND=1` before a second parse. Full long opts with `--opt=val` → GNU `getopt` instead:
```bash
opts=$(getopt -o yn -l dry-run,yes -- "$@") || exit 2; eval set -- "$opts"
```

## Subcommand dispatch (`git`-style)
```bash
cmd="${1:-}"; shift || true
case "$cmd" in
  backup)  backup "$@" ;;
  restore) restore "$@" ;;
  ""|--help|-h) usage; exit 0 ;;
  *) echo "unknown command: $cmd" >&2; exit 2 ;;
esac
# Each subcommand has its OWN getopts loop (reset OPTIND=1 first).
```

## CLI design rules
- `--help` + `--dry-run` on every destructive script. `--help` prints usage and exits 0.
- `--yes` gates real runs: without it, print plan and exit. `run()` wrapper routes everything:
```bash
run() { if (( DRY_RUN )); then printf '[DRY] %s\n' "$*" >&2; else "$@"; fi; }
```
- Exit codes: `0` ok, `1` error, `2` usage error. `die "msg" 2` for bad flags.
- Required positional: `target="${1:?usage: $0 [--dry-run] <dir>}"`.

## Pitfalls

- Forgetting `shift` — flags leak into `"$@"` file loops and get treated as filenames.
- getopts uses OPTIND; a Bash function can use local OPTIND=1 to isolate a parse. At top level reset it deliberately before reuse.
- GNU getopt's quoted-output pattern can be appropriate exactly as documented; do not eval user-built text. A manual case loop is valid when its grammar is explicit and tested, including whether --opt=value is supported.

## Try it

```bash
bash -c '
DRY_RUN=0; YES=0
set -- --dry-run --yes foo
while getopts ":yn-:" opt; do case "$opt" in
 -) case "$OPTARG" in dry-run) DRY_RUN=1;; yes) YES=1;; esac;;
 y) YES=1;; n) DRY_RUN=1;; esac; done
shift $((OPTIND-1)); echo "dry=$DRY_RUN yes=$YES left=$*"'
# dry=1 yes=1 left=foo
```

## Optional scratch drills (inside bash-cli/work)

1. `flags.sh`: `-y/--yes`, `-n/--dry-run`, `-o FILE` (with arg) — print parsed values + remaining positionals; exit 2 on unknown.
2. `confirm.sh`: without `--yes`, print plan and exit 0; with `--yes`, execute via `run()`. Prove `--dry-run --yes` still only prints.
3. `usage.sh`: `--help` output (usage, flags, examples, exit codes) + required `$1` via `:?`.

## Related

- [[08-bash-functions-scope|Functions]]
- [[13-bash-capstone|Capstone]]

Sources: [Bash builtins / getopts](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html), [getopt](https://man7.org/linux/man-pages/man1/getopt.1.html). Gate: assert usage status 2 separately from runtime status 1 and prove dry-run has no filesystem side effects.
