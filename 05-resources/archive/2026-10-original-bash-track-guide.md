---
created: 2026-10-08
updated: 2026-10-08
---

# Original Bash track guide — historical reference

Archived during the learning-system rebuild. Follow [[00-how-to-use-track]] for current lab locations, compatibility and behavioral gates. Previous environment-verification claims below are historical.

Self-contained Bash-as-a-language course. No external course needed. Separate from `03-scripting/` (automation patterns) — this is the *language itself*.

## Order (each builds on the last)

| # | Note | What you gain |
|---|---|---|
| 01 | [[01-shell-model\|Shell Model]] | commands, lists/pipelines, exit codes, `$@` matrix, `man bash` map |
| 02 | [[02-bash-expansions\|Expansions]] | the order model + full arithmetic — the single most important note |
| 03 | [[03-quoting-splitting-globbing\|Quoting, Splitting, Globbing]] | quoting, `extglob`, why quoting fixes 80% of bugs |
| 04 | [[04-bash-parameters\|Parameters]] | full `${}` family + `${var@Q}` transforms |
| 05 | [[05-bash-arrays\|Arrays]] | indexed + assoc + `mapfile` |
| 06 | [[06-bash-conditionals\|Conditionals]] | `[[ ]]/(( ))/case/=~`, full primaries |
| 07 | [[07-bash-loops\|Loops]] | `for/while/until/select` |
| 08 | [[08-bash-functions-scope\|Functions]] | `local`, dynamic scope, return/exit |
| 09 | [[09-bash-redirections\|Redirections]] | fds, `<()>`, heredocs, `tee`, `/dev/*`, `noclobber` |
| 10 | [[10-bash-traps-jobs\|Traps & Jobs]] | signals, `trap`, `&/wait -n/disown` |
| 11 | [[11-bash-text-processing\|Text Processing]] | orchestration bridge: bash + `grep/sed/awk/sort` (tools live in scripting track) |
| 12 | [[12-bash-args-options\|Args & Options]] | `$@`, `getopts`, subcommands, CLI design |
| 14 | [[14-set-shopt-strict-debug\|Set, Shopt, Strict Mode, Debugging]] | `set -euo pipefail` truth, `shopt` catalog, `set -x/PS4` |
| 15 | [[15-builtins-printf-read-exec-eval\|Builtins: printf, read, exec, eval]] | `printf -v/%q`, `read` flags, `exec/source/command`, `eval` safety |
| 16 | [[16-shell-vars-index\|Shell Variables Index]] | Bourne + `BASH_*` reference table |
| 13 | [[13-bash-capstone\|Capstone]] | spec: build one script using everything (portable + Arch variants) |
| 90 | [[90-bash-language-protips\|Language Protips]] | gotcha log, append as you bleed (tagged by note) |

## How to study each note

1. Read the concept (5 min).
2. Run every `Try it` block by hand in a scratch terminal — verified on `bash 5.3.20` here.
3. Do the 3 exercises at the bottom into `03-exercises/bash-lang/NN-topic/` as `.sh` files.
4. Gate before moving on: `bash -n` clean, `shellcheck` clean, and you can explain the output without re-running.

```bash
mkdir -p ~/learning/bash-lang/02-expansions
cd ~/learning/bash-lang/02-expansions
bash -n ex1.sh && shellcheck ex1.sh && bash ex1.sh
```

## Rules
- Interactive shell here is `zsh` — always test with `bash -c '...'` or `#!/usr/bin/env bash` scripts so zsh-isms don't leak in.
- Quote-first: if in doubt, double-quote. Unquote deliberately, never accidentally.
- Reference: `man bash` (sections EXPANSION, PARAMETERS, ARRAYS, Compound Commands, Conditional Expressions, Redirections). This track teaches you to *read* it, not replace it.
- Check version first: `echo "$BASH_VERSION"` (here `5.3.20`). macOS ships bash 3.2 — no assoc arrays, no `**`, no `&>>`, no `${v^}`/`${v@Q}`. See [[16-shell-vars-index\|Shell Variables Index]] for compat notes.

## `man bash` → note map

| `man bash` section | Lives here |
|---|---|
| DEFINITIONS, RESERVED WORDS, SHELL GRAMMAR (lists/pipelines) | [[01-shell-model\|01]] |
| EXPANSION, ARITHMETIC EVALUATION | [[02-bash-expansions\|02]] |
| QUOTING, Word Splitting, Pathname Expansion/Pattern Matching | [[03-quoting-splitting-globbing\|03]] |
| PARAMETERS (incl. `${var@op}`) | [[04-bash-parameters\|04]] |
| ARRAYS | [[05-bash-arrays\|05]] |
| Compound Commands, Conditional Expressions | [[06-bash-conditionals\|06]], [[07-bash-loops\|07]] |
| FUNCTIONS | [[08-bash-functions-scope\|08]] |
| REDIRECTION | [[09-bash-redirections\|09]] |
| SIGNALS, JOB CONTROL, `trap/wait/jobs/kill` | [[10-bash-traps-jobs\|10]] |
| SHELL BUILTIN COMMANDS (`set/shopt`), Modifying Shell Behavior | [[14-set-shopt-strict-debug\|14]] |
| SHELL BUILTIN COMMANDS (`printf/read/exec/eval/source`) | [[15-builtins-printf-read-exec-eval\|15]] |
| PARAMETERS/Bourne + Bash Variables | [[16-shell-vars-index\|16]] |
| COMMAND EXECUTION, Exit Status, Environment | [[01-shell-model\|01]] + [[15-builtins-printf-read-exec-eval\|15]] |

## Non-goals (explicitly out of this track)
- Interactive only: readline/editing, history expansion (`! !! !$`), programmable completion, prompt (`PS1`, `PROMPT_COMMAND`). `!` pipeline negation IS in track (see [[01-shell-model\|01]]); `!` history expansion is NOT.
- `coprocess` (`coproc`): exists, rarely needed — use `<()`/`$()` instead (one-liner in [[09-bash-redirections\|09]]).
- Aliases in scripts: off by default (`expand_aliases`), use functions. Startup files (`.bashrc`, `BASH_ENV`) belong to interactive track.
- Restricted shell / POSIX `sh` portability: write `#!/usr/bin/env bash`, use `shellcheck -s bash`. POSIX boxes appear where a bashism has a portable fallback.

## Related
- [[00-bash-basics|Bash Basics]] (scripting track — automation, not language)
- [[90-bash-language-protips|Language Protips]]
- [[13-bash-capstone|Capstone]]
