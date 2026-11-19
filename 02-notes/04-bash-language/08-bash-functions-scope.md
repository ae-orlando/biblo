---
created: 2026-10-08
updated: 2026-10-21
---

# 08 — Functions and Scope

> Prerequisite: conditionals and parameters. Outcome: identify dynamic-scope dependencies and preserve failures across helper boundaries. Practice: `bash-cli` and `bash-jobs` in [[practice-catalog]].

## Mental model

Functions package logic + take `$1..$n` (their own positional params). `local` exists **only** in functions. Scope is **dynamic**, not lexical: a callee sees the caller's locals. `return N` sets function status (0-255); `exit N` kills the whole script. `main "$@"` + source-guard keeps files both runnable and testable.

```bash
greet() { local name="$1"; echo "hi $name"; return 0; }
greet "orlando"; echo $?   # hi orlando / 0
```

## Dynamic scope (the surprise)
```bash
x=global
outer() { local x=outer-local; inner; }
inner() { echo "inner sees x=$x"; }
outer   # inner sees x=outer-local — NOT global. Callees see caller locals.
```
Consequence: name locals distinctively, never rely on globals inside helpers without passing args.

## `local` gotchas
```bash
f() { local y=$(false); echo $?; }; f   # 0 — MASKS failure (SC2155). Split:
g() { local y; y=$(false); echo $?; }; g  # 1 — real status
local x   # outside function: `local: can only be used in a function`
```

## `return` vs `exit`
```bash
fret() { return 42; }; fret; echo $?   # 42 — function only, wraps mod 256 (300→44)
bash -c 'f(){ exit 7; }; f; echo unreached'  # exit ends the PROCESS
# rule: return in functions, exit in main/top-level, die() for fatal errors
```

## Structure pattern
```bash
#!/usr/bin/env bash
# Avoid changing the caller's options merely by sourcing this file.
log() { printf '[INFO] %s\n' "$*" >&2; }
die() { printf '[ERROR] %s\n' "$*" >&2; exit 1; }
parse_args() { local f="$1"; echo "file=$f"; }
main() { set -euo pipefail; local target="${1:?usage: $0 <dir>}"; parse_args "$target"; }
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then main "$@"; fi
# sourced? guard false → only definitions load. Executed? main runs.
# FUNCNAME is available for diagnostics inside functions; do not print on import.
```

Recursion works (subshell per `$( )` call):
```bash
fact() { local n=$1; (( n <= 1 )) && { echo 1; return; }; echo $(( n * $(fact $((n-1))) )); }
fact 5  # 120
```

## Pitfalls

- `local x=$1` when `$1` unset under `set -u` aborts — `${1:?}` or default first.
- Forgetting the source-guard: sourcing `install.sh` from tests RUNS the installer. Guard every executable lib.
- return is valid in a function or sourced script; outside both it errors. exit in a sourced library can terminate the caller's shell. A source guard does not protect unrelated top-level commands/options from running.

## Try it

```bash
bash -c 'x=global; outer() { local x=L; inner; }; inner() { echo "$x"; }; outer'
bash -c 'f() { local y=$(false); echo "masked:$?"; }; f; g() { local y; y=$(false); echo "real:$?"; }; g'
bash -c 'fact() { local n=$1; (( n <= 1 )) && { echo 1; return; }; echo $(( n * $(fact $((n-1))) )); }; fact 5'
```

## Optional scratch drills (inside bash-cli/work)

1. `scope.sh`: reproduce the dynamic-scope demo, then fix by passing `x` as an arg so `inner` needs no globals.
2. `mask.sh`: show SC2155 masked vs split `local`/assign with `$?` proof; run `shellcheck` to confirm it flags the masked form.
3. `lib.sh`: two functions + guarded `main`; prove `source lib.sh` defines but doesn't run, and `./lib.sh arg` runs.

## Related

- [[12-bash-args-options|Args & Options]]
- [[10-bash-traps-jobs|Traps & Jobs]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]] (`set -E/-T`, `functrace`)
- [[15-builtins-printf-read-exec-eval|Builtins]] (`source`-guard, `export -f`, `caller`)
- [[16-shell-vars-index|Shell Variables Index]] (`FUNCNAME/BASH_SOURCE`)

Sources: [Shell functions](https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html). Gate: explain which helpers mutate shared state and prove that a failed operation is not masked by a declaration builtin.
