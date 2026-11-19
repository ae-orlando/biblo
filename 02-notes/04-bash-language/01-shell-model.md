---
created: 2026-10-08
updated: 2026-10-21
---

# 01 — Shell Model (commands, lists, pipelines, exit codes)

> Outcome: explain argument boundaries, process status and execution context. Practice: `bash-quoting` and `bash-pipeline` in [[practice-catalog]]. The scratch tasks below are self-authored inside a related lab's work directory.

## Mental model

Bash reads a line, expands it (see [[02-bash-expansions|Expansions]]), runs the first word as a command, stores the result code in `$?`. `0` = success, `1-255` = failure. `if`/`while`/`&&`/`||` branch on that code — there are no booleans, only exit codes.

Parsing recognizes reserved words and can expand aliases; that is not one linear command-lookup list. For an ordinary command name without a slash, Bash normally searches functions, builtins, then hashed/PATH executables. A slash selects a pathname. Inspect actual resolution with type:
```bash
type cd echo ls if myfunc 2>&1
type -a ls          # ALL matches (alias/function/builtin/file)
command -v python3  # preferred over which (sees builtins/functions)
command ls ...      # bypass function/alias, run builtin-or-file
builtin echo hi     # force builtin; enable -n echo disables it
hash -t ls 2>/dev/null || true  # cached PATH lookup
```

## Core facts

Exit codes (conventions, not enforced):
```bash
true; echo $?    # 0 success
false; echo $?   # 1 general failure
ls /nonexistent 2>/dev/null; echo $?   # 2 (tool-specific)
bash -c 'nonexistent_xyz'; echo $?     # 127 = command not found
bash -c '/dev/null' 2>/dev/null; echo $?  # 126: a found path cannot be executed
bash -c 'kill -TERM $$' 2>/dev/null; echo $?  # 128+15=143 — killed by signal N → 128+N
# Functions: return N wraps mod 256 (return 300 → rc 44). exit N ends the PROCESS.
```

Lists branch on codes (precedence: `&&`/`||` bind tighter than `;`/`&`; left-associative):
```bash
mkdir -p a && cd a && echo "in a"   # && = run if previous SUCCEEDED
cd /nonexistent 2>/dev/null || echo "fallback"   # || = run if previous FAILED
# ; = always run next. Newline = same as ;.
# & = run async in subshell, stdin defaults to /dev/null, rc is 0 immediately
sleep 1 & echo "launched $!"
```

Pipelines + negation + timing:
```bash
false | true; echo "${PIPESTATUS[@]} $?"  # 1 0 / 0 — PIPESTATUS has EVERY stage, $? is LAST only
set -o pipefail; false | true; echo $?; set +o pipefail  # 1 — pipefail = last non-zero (see note 14)
! false; echo $?          # 0 — ! negates pipeline rc (! failing-command = success)
time sleep 0.1            # reserved word: times pipeline; TIMEFORMAT controls output
false |& cat 2>&1 | head  # |& = 2>&1 | (pipe stdout AND stderr)
```

`$?` is volatile — any command overwrites it. Save immediately:
```bash
some_cmd
rc=$?
echo "rc=$rc"
# Save immediately in the current shell: statuses=("${PIPESTATUS[@]}")
```

Special vars + `"$@"` vs `"$*"` matrix (the #1 arg bug):
```bash
echo "$# args: $@ | prog:$0 pid:$$ flags:$- last-arg:$_ bg-pid:$! status:$?"
set -- a b c; echo "$# $1 $2 ${10:-none}"  # ${10} needs braces
shift; echo "$@"   # drops $1
shift 2; echo "$# $@"  # shift N; fails (rc 1) if N > $#
set -- "a b" "c*d"
printf '<%s>\n' "$@"   # <a b> <c*d> — CORRECT: one word per arg, no split/glob
printf '<%s>\n' "$*"   # <a b c*d> — ONE word joined with first char of IFS (space)
printf '<%s>\n' $@     # splits+globs — NEVER (SC2068). $* unquoted is worse.
# Empty-list under set -u: "$@" is safe (expands to nothing), $* may error on old bash — always "$@" in loops.
for f in "$@"; do echo "file=$f"; done
```

Subshell `( )` vs group `{ }`:
```bash
( z=1 ); echo "${z-unset}"   # unset — subshell changes are lost
{ z=2; }; echo "$z"          # 2 — group runs in current shell (needs spaces + ;)
(cd /tmp; pwd); pwd          # subshell cd doesn't leak — the pattern for "do X over there"
# Pipeline stages normally use subshell environments; lastpipe can change the
# last stage when job control is off. Do not assume a pipe-fed read updates x.
```

Directory stack (belongs here, not just `cd`):
```bash
pushd /tmp >/dev/null; pwd; dirs -v; popd >/dev/null; pwd
pushd -n /other  # stack without cd; dirs -p to list; DIRSTACK array holds it
```

## Arch note
`man bash` is the textbook (`man-db` package). Sections to know exist: NAME, DEFINITIONS, RESERVED WORDS, PARAMETERS, EXPANSION, ARRAYS, Compound Commands, Conditional Expressions, Redirections, FUNCTIONS, JOB CONTROL. `info bash` is the same content hyperlinked.

## Pitfalls

- `if [ $? -ne 0 ]` — write `if ! cmd; then` (SC2181). Keeps `$?` from being clobbered.
- Assuming `$?` survives an `echo` — it doesn't. Save first. Same for `PIPESTATUS` — read it before ANY other command.
- `( exit 1 )` in a function "returns" 1 from subshell only — use `return 1`.
- `for f in $@` / `$*` unquoted — splits and globs. Always `for f in "$@"`.
- Forgetting `&` stdin is `/dev/null` — background `read` gets EOF instantly unless redirected.

## Try it

```bash
bash -c 'false || echo "or-ran"; true && echo "and-ran"'
bash -c '(x=5); echo "${x-unset}"; { y=6; }; echo "$y"'
bash -c 'set -- a b c; echo "$#"; shift; echo "$@"'
type cd; command -v bash
bash -c 'set -- "a b" "c"; printf "<%s>\n" "$@"; printf "<%s>\n" "$*"'
bash -c 'false | true; echo "${PIPESTATUS[@]} $?"; ! false; echo "$?"'
bash -c 'pushd /tmp >/dev/null && pwd && popd >/dev/null && pwd'
```

## Optional scratch drills (inside a related lab's work directory)

1. `rc.sh`: run three commands (one failing), save each `$?` to `rc1/rc2/rc3`, print them. Prove `echo` between command and check breaks it, then fix.
2. `guard.sh`: `cd "$1" && ls` — show it skips `ls` on bad dir; rewrite with `||` fallback message.
3. `subshell.sh`: function that `cd`s in a subshell, prints `pwd` inside and outside. Confirm outer dir unchanged.
4. `args-matrix.sh`: `set -- "a b" "c*d"` — print `"$@"` vs `"$*"` vs unquoted with `printf '<%s>\n'`; comment which is safe. Run under `set -u` with empty args.
5. `pipe-status.sh`: `false | true` — print `$?` vs `"${PIPESTATUS[@]}"`, then with `set -o pipefail`; show `! false` rc.

## Related

- [[02-bash-expansions|Expansions]]
- [[06-bash-conditionals|Conditionals]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]]
- [[15-builtins-printf-read-exec-eval|Builtins]]

Sources: [Bash command execution](https://www.gnu.org/software/bash/manual/html_node/Executing-Commands.html), [exit status](https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html). Gate: explain the observed status and preserve the original pipeline statuses before another command changes them; pass the linked behavioral lab.
