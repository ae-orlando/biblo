---
created: 2026-10-08
updated: 2026-10-21
---

# 16 — Shell Variables Index (Bourne + `BASH_*`)

> Lookup reference, not a memorization gate. Use a real question from `bash-cli`, `bash-jobs` or `bash-capstone` in [[practice-catalog]], then explain the variable's lifetime and scope.

Quick lookup. Bourne vars are inherited/env-relevant; `BASH_*` exist only inside bash. Inspect any with `declare -p NAME`. Full list: `man bash` PARAMETERS + Shell Variables.

## Positional + special (see also [[01-shell-model|01]])
| Var | Meaning | Note |
|---|---|---|
| `$1..$n`, `${10}` | positionals | braces past 9; functions have their own |
| `$#` | count | `shift` decrements |
| `$@` / `$*` | all args | quoted `"$@"` = one word each (ALWAYS); `"$*"` = one word joined by IFS |
| `$?` | last rc | volatile; `PIPESTATUS` for full pipeline |
| `PIPESTATUS[]` | every pipeline rc | read BEFORE any other command |
| `$$` / `$!` | self PID / last bg PID | `wait "$!"` reaps |
| `$0` / `$_` | prog name / last arg | `$0` ≠ sourced file — use `BASH_SOURCE[0]` in libs |
| `$-` | flags (`himBH`) | `[[ $- == *i* ]]` = interactive? |
| `OPTARG`/`OPTIND` | `getopts` value/index | reset `OPTIND=1` before re-parse |

## Bourne / env vars
| Var | Meaning |
|---|---|
| `HOME PWD OLDPWD` | home, current, previous (`cd -` uses it) |
| `PATH IFS` | lookup dirs (`:`-sep) / split chars (default space-tab-newline) |
| `OPTARG OPTIND REPLY` | `getopts` + `select`/`read` default targets |
| `PS1 PS2 PS3 PS4` | interactive prompt, continuation, `select`, `set -x` prefix (`PS4='+ ${LINENO}: '`) |
| `LANG LC_ALL TZ` | locale/timezone (sorting, `[[ < ]]`, `printf %T`) |
| `TEXTDOMAIN TEXTDOMAINDIR` | `$"..."` gettext lookups |
| `ENV BASH_ENV` | sourced for `sh` / non-interactive bash |
| `HISTFILE HISTSIZE HISTCONTROL HISTIGNORE` | history persistence (interactive) |
| `TMOUT MAILCHECK` | idle/logout + mail timers |

## Bash vars (verify with `echo "$BASH_VERSION"`)
| Var | Meaning | Example |
|---|---|---|
| `BASH_VERSION` | version | `5.3.20(1)-release` here; macOS ships 3.2 (no assoc/`**`/`@Q`) |
| `BASH_SOURCE[] BASH_LINENO[] FUNCNAME[]` | call stack | `"${BASH_SOURCE[0]}" == "$0"` guard; `caller` prints one frame |
| `BASH_REMATCH[]` | `[[ =~ ]]` groups | `[0]` whole, `[1..]` captures |
| `RANDOM SECONDS EPOCHSECONDS LINENO SRANDOM` | rng / timers / line | `RANDOM=42` seeds; `SECONDS=0` reset |
| `GROUPS UID EUID HOSTNAME OSTYPE MACHTYPE SHLVL` | identity | `(( EUID == 0 ))` root check |
| `DIRSTACK` | pushd/popd directory stack | dirs -v views it |
| `BASH_COMMAND` | current command | used in `DEBUG`/`ERR` traps |
| `TIMEFORMAT` | `time` output | `TIMEFORMAT=%R` seconds only |
| `GLOBIGNORE` | hide glob matches | `GLOBIGNORE='*.bak'`; unset to restore |
| `BASH_XTRACEFD` | `set -x` target fd | `exec 9>trace; BASH_XTRACEFD=9` |

## Compat notes
- bash 3.2 (macOS default): NO `declare -A`, NO `**`/`globstar`, NO `&>>`/`|&` (use `>f 2>&1`), NO `^/,,/@Q`, NO `inherit_errexit`/`wait -n`. Install newer bash or code to 3.2 subset.
- Feature introductions differ: associative arrays/case conversion are Bash 4.0; printf's time format is 4.2; namerefs and wait -n are 4.3; mapfile -d and ${v@Q} are 4.4. A single “4.2+” label is insufficient. Labs target Bash 5+.

## Try it

```bash
bash -c 'echo "$BASH_VERSION"; RANDOM=1; echo "$RANDOM $RANDOM"; SECONDS=0; sleep 0.1; echo "$SECONDS"'
bash -c 'f(){ echo "func:${FUNCNAME[0]} src:${BASH_SOURCE[0]} line:${LINENO}"; caller; }; f'
bash -c 'GLOBIGNORE="*.bak"; echo "gi=$GLOBIGNORE"; unset GLOBIGNORE'
```

## Related

- [[01-shell-model|Shell Model]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]]
- [[15-builtins-printf-read-exec-eval|Builtins]]

Sources: [Bash variables](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html), [Bash release history](https://tiswww.case.edu/php/chet/bash/NEWS). Verify the actual target runtime when portability matters; see [[implementation-status]].
