---
created: 2026-10-08
updated: 2026-10-21
---

# Robust Bash Scripts (set -euo pipefail, traps, flags)

> Prerequisites: Bash language semantics, especially [[14-set-shopt-strict-debug]] and [[10-bash-traps-jobs]]. Practice: `bash-cli`, `bash-pipeline` and `bash-jobs` in [[practice-catalog]]. The behavioral contracts and tests outrank a generic template.

## Mental model

Bash status handling is contextual; flags are not exception semantics. A trap handles specific ordinary exit/signal paths but cannot guarantee cleanup after SIGKILL or power loss. Dry-run is useful only when every side-effect path, including setup/redirection, is non-writing. Choose a template for the tool's actual contract rather than prescribing one for every script.

Copy-paste template:
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

log()  { printf '[INFO] %s\n' "$*" >&2; }
die()  { printf '[ERROR] %s\n' "$*" >&2; exit "${2:-1}"; }

DRY_RUN=0
YES=0
while getopts ":yn-:" opt; do
  case "$opt" in
    -) case "$OPTARG" in
         dry-run) DRY_RUN=1 ;;
         yes) YES=1 ;;
         *) die "unknown --$OPTARG" 2 ;;
       esac ;;
    y) YES=1 ;;
    n) DRY_RUN=1 ;;
    :) die "missing arg -$OPTARG" 2 ;;
    \?) die "bad -$OPTARG" 2 ;;
  esac
done
shift $((OPTIND - 1))

run() {
  if (( DRY_RUN )); then log "DRY: $*"; else "$@"; fi
}

main() {
  log "args left: $*"
  run printf '%s\n' 'safe training operation'
}
[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"
```

## What strict mode does

| Flag | Meaning | Gotcha |
|---|---|---|
| `set -e` | exit on simple-command failure | Ignored in `if`/`while` tests, `&&`/`\|\|` lists, `!` pipelines. `false \|\| true` does NOT exit. |
| `set -u` | unset var = error+exit | Use `${VAR:-default}` / `${VAR:=default}` for optional vars. |
| `set -o pipefail` | pipeline = last non-zero, else 0 | Without it `false \| true` exits 0 (only last counts). |

Verified locally: `bash -c 'set -euo pipefail; false | true; echo hi'` prints **nothing** — the pipeline fails (1) and `-e` exits before `echo`. Without `pipefail` it would print `hi`. This is exactly why installers need it: `download | install` must fail if download fails.

When NOT to use: sourced libraries (poisons caller), scripts needing fine recovery (use explicit `cmd || return 1` instead).

## Traps + temp dirs
```bash
mkdir -p .practice-runtime/scratch
tmp=$(mktemp -d .practice-runtime/scratch/cleanup.XXXXXX)
cleanup() { rmdir -- "$tmp"; }  # empty owned scratch directory only
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# single-quoted 'rm ... "$tmp"' expands at EXIT, not now. Never unquoted $tmp.
# EXIT does not run after SIGKILL. Returning INT/TERM cleanup alone need not exit.
```

## Logging
```bash
log() { printf '[INFO] %s\n' "$*" >&2; }        # >&2 keeps stdout clean for pipes
die() { printf '[ERROR] %s\n' "$*" >&2; exit 1; }
# colors only on tty (no escapes in logs):
if [[ -t 2 ]]; then RED=$'\e[31m'; RST=$'\e[0m'; else RED=''; RST=''; fi
exec > >(tee -a setup.log) 2>&1   # duplicate all to log file
```

## Arch note

Tools not installed here but in `extra` (verified `pacman -Si`): `shellcheck 0.11.0`, `shfmt 3.14.1`. Install once:
```bash
sudo pacman -S shellcheck shfmt
shellcheck install.sh     # SC2086, SC2046, SC2181 — fix all
shfmt -i 2 -ci -bn -d install.sh   # -d diff first, -w to write
bash -n install.sh        # syntax only, no exec
bash -x install.sh --dry-run       # trace; PS4='+ ${BASH_SOURCE}:${LINENO}: ' for location
```

## Pitfalls

- `local v=$(cmd)` hides failure — split into two lines.
- `trap "rm -rf $tmp"` double-quoted expands NOW (empty) — single-quote the body.
- `rm -rf "$tmp/"` with unset var under `set -u` — use `"${tmp:?}"`.
- `getopts` needs `OPTIND=1` reset before second parse; `shift $((OPTIND-1))` drops parsed opts.

## Try it

```bash
bash -n 03-exercises/bash-lang/02-cli/starter/main.sh
bash -c 'set -o pipefail; false | true; echo "exit:$?"'
bash -c 'set -u; echo "${MISSING:-fallback}"'
```

## Related

- [[00-bash-basics|Bash Basics]]
- [[30-script-workflow|Script Workflow]]
- [[20-arch-automation|Arch Automation]]

Sources: [Set builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html), [BashFAQ/105](https://mywiki.wooledge.org/BashFAQ/105), [ShellCheck](https://www.shellcheck.net/wiki/). Gate: explain a caught failure, prove unchanged output on error/dry-run, and show owned workers are reaped. Syntax-check scripts, not Markdown files. Host installation examples require a VM/separate approval; the launcher uses a vault-local linter.
