---
created: 2026-10-08
updated: 2026-10-21
---

# 14 — Set, Shopt, Strict Mode, Debugging

> Prerequisites: execution contexts and pipelines. Outcome: choose explicit failure handling rather than assuming flags provide exception semantics. Practice: `bash-cli`, `bash-pipeline` and `bash-jobs` in [[practice-catalog]].

## Mental model

set -o controls shell options (not just POSIX behavior); shopt controls additional Bash options. The conventional “strict mode” flags have contextual limits and are not exception handling. Trace deliberately, remembering that expanded commands can reveal secrets.

## set -o essentials (reference; current checks are recorded separately)
```bash
set -o                    # list all; set -o errexit == set -e
set -euo pipefail         # errexit + nounset + pipefail (see below)
set -x; PS4='+ ${BASH_SOURCE}:${LINENO}: '  # tracing (see Debugging)
set -f; set -o noglob     # same thing: disable globbing (not splitting)
set -C; set -o noclobber  # > refuses to clobber; override once with >|
set -E; set -o errtrace   # ERR trap inherits in functions/subshells
set -T; set -o functrace  # DEBUG/RETURN traps inherit
set -m                    # monitor: job control in scripts (for jobs/fg/bg)
set -v                    # verbose: print lines as READ (before expansion); -x prints AFTER
set -- a b c              # reset positionals; set -- clears $@
set -u; echo "${undef:-def}"  # nounset-safe default; ${undef:?msg} aborts with msg
```

## `set -e` truth (errexit blind spots — BashFAQ/105)
`set -e` is IGNORED when the failing command is:
- part of `if`/`while`/`until` test, `&&`/`||` list (except final), `!` negation,
- last command in a pipeline under test, or in `$( )`/subshell assigned in those contexts.

```bash
set -e
false || echo rescued        # NOT fatal (|| list)
if false; then :; fi         # NOT fatal (if test)
false | true; echo "rc:$?"   # pipeline rc is LAST (0) — use pipefail + PIPESTATUS
(( i++ ))                    # FATAL when i==0 (result 0 = false) → ((++i)) || true
grep -q x file || true       # intentional-fail idiom: append || true
```

## `set -u` + `pipefail` rules
```bash
set -u
echo "${opt:-default}"       # :- / - / := / :? all work under -u; bare $opt aborts
echo "$@"                    # SAFE even when empty (expands to nothing)
# "${arr[@]}" on EMPTY array aborts on bash <4.4 — guard: ${arr[@]:-}
set -o pipefail              # pipeline rc = last NON-ZERO, else 0
false | true; echo $?        # 1 with pipefail, 0 without
cmd | tee log; test "${PIPESTATUS[0]}" -eq 0  # PIPESTATUS must be read FIRST
```

## `shopt` catalog (the ones that matter)
```bash
shopt                              # list; shopt -s on, -u off, -p printable for scripts
shopt -s extglob globstar nullglob failglob dotglob nocaseglob  # patterns (see note 03)
shopt -s nocasematch               # case/[[ == ]] case-insensitive
shopt -s lastpipe                  # eligible last stage may use current shell when job control is off
shopt -s inherit_errexit            # set -e inherits in $( ) subshells (bash 4.4+)
shopt -s checkjobs huponexit        # warn on exit with jobs / SIGHUP background on exit
shopt -s autocd cdable_vars        # interactive conveniences (NOT for scripts)
shopt -s checkwinsize               # update LINES/COLUMNS after each command (on by default here)
```

## Debugging
```bash
bash -n script.sh                  # syntax check only (no exec)
bash -x script.sh                  # trace every expanded command
export PS4='+ ${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]:-main}: '
export BASH_XTRACEFD=2             # or =9 with exec 9>trace.log
trap 'echo "ERR at $LINENO: $BASH_COMMAND" >&2' ERR  # needs set -E in functions
trap 'echo "+ $BASH_COMMAND" >&2' DEBUG  # step-trace (noisy; extdebug for more)
caller; echo "${FUNCNAME[*]} ${BASH_LINENO[*]}"  # call stack in error paths
```

## Pitfalls

- `set -e` + `(( x++ ))` from 0 kills the script. Pre-increment or `|| true`.
- `set -u` + empty `"$1"` in functions aborts — use `"${1:-}"` / `"${1:?usage}"`.
- `PIPESTATUS` after ANY command (even `echo`) is stale. Save immediately.
- nullglob affects unmatched pathname expansion, not existence tests inside [[ ]]. Restore the prior option state, not blindly “off,” or confine changes to a subshell.
- macOS bash 3.2: no `globstar`, no `inherit_errexit`, no `assoc`. Test `[[ -n ${BASH_VERSION} ]]`.

## Try it

```bash
bash -c 'set -e; false || echo rescued; if false; then :; else echo if-rescued; fi'
bash -c 'set -o pipefail; false | true; echo "rc:$? ${PIPESTATUS[*]}"'
bash -c 'set -u; echo "${u:-def}"; set --; printf "<%s>\n" "$@" | cat -A; echo ok'
bash -c 'PS4="+L\${LINENO}: "; set -x; v=1; echo "v=$v" 2>&1 | head -3'
bash -c 'shopt -s extglob; [[ foo123 == +(a|f)* ]] && echo extglob-on'
```

## Optional scratch drills (inside bash-pipeline/work)

1. `errexit.sh`: with `set -e`, show `false ||`, `if false`, `false | true` survivals vs bare `false` death (run each in subshells to keep testing).
2. `pipefail.sh`: `false | true` with/without `pipefail`; capture both `PIPESTATUS` entries to variables before any other command.
3. `trace.sh`: `PS4` + `set -x` on a 5-line script; redirect trace to `trace.log` via `BASH_XTRACEFD=9`.

## Related

- [[01-shell-model|Shell Model]] (`$?`, `PIPESTATUS`, `!`)
- [[03-quoting-splitting-globbing|Quoting/Splitting/Globbing]] (`shopt` patterns)
- [[10-bash-traps-jobs|Traps & Jobs]] (`ERR/DEBUG/RETURN`, `set -E/-T`)

Sources: [The Set builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html), [The Shopt builtin](https://www.gnu.org/software/bash/manual/html_node/The-Shopt-Builtin.html), [BashFAQ/105](https://mywiki.wooledge.org/BashFAQ/105). Gate: show the failed command/status and a caught behavioral regression, not merely a clean linter.
