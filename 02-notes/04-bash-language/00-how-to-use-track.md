# Bash learning path — semantics before automation

This track teaches Bash as a language. [[linux-learning-path]] teaches operating-system diagnosis; `03-scripting/` applies both to automation. Cross-link them instead of duplicating competing explanations.

Use [[baseline-diagnostic]] to place yourself. The current lab target is **Bash 5+ with GNU/Linux tools**, verified separately in [[implementation-status]]. Your interactive shell may be zsh; run Bash snippets in `bash -c` or a Bash script. Do not assume macOS's Bash 3.2 or BSD utility flags are compatible.

## Sequence and practice

| Unit | Read | Behavioral evidence |
| --- | --- | --- |
| Execution and words | [[01-shell-model]], [[02-bash-expansions]], [[03-quoting-splitting-globbing]] | `bash-quoting`: arbitrary names and NUL framing |
| Data/control | [[04-bash-parameters]], [[05-bash-arrays]], [[06-bash-conditionals]], [[07-bash-loops]] | Use validation and preserved input boundaries in `bash-cli` |
| Structure and streams | [[08-bash-functions-scope]], [[09-bash-redirections]], [[11-bash-text-processing]], relevant [[15-builtins-printf-read-exec-eval]] | `bash-pipeline`: no success output after a late parse failure |
| Interfaces and errors | [[12-bash-args-options]], [[14-set-shopt-strict-debug]] | `bash-cli`: usage/runtime separation, dry-run, atomic output replacement |
| Lifecycles | [[10-bash-traps-jobs]], remaining builtins | `bash-jobs`: owned workers cleaned/reaped on normal/TERM exit |
| Integration | [[16-shell-vars-index]] as reference, [[13-bash-capstone]] | `bash-capstone`: deterministic read-only inventory and change request |

Specifications, starters, fixtures, tests and hints are in [[practice-catalog]]. Example:

```bash
python3 90-tools/practice.py start bash-quoting
python3 90-tools/practice.py check bash-quoting
```

Edit the created lab `work/`, never the supplied reference. Older per-note exercise filenames are **self-authored scratch drills**, not pre-existing files or required old directory names. Keep them under a related lab's work directory. No new work is routed into ~/learning/ automatically.

## Gates and references

Use bash -n and ShellCheck as helpful static checks, **then** run behavioral checks. Explain exit status, splitting/globbing, input framing, side effects and failure cleanup. Introduce a bug, observe a failing case, repair it, and meet a changed requirement. Clean syntax is not a language-mastery certificate.

Consult man bash / the [GNU Bash manual](https://www.gnu.org/software/bash/manual/) and [ShellCheck wiki](https://www.shellcheck.net/wiki/). Do not memorize every special variable before building. Use [[16-shell-vars-index]] when a real question arises.

[[90-bash-language-protips]] preserves earlier gotcha entries; dated correction annotations distinguish historical observations from current guidance. [[study-and-review]] defines completion and retention.
