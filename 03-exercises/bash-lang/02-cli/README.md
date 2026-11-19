# Lab: safe CLI and atomic report replacement

**ID:** `bash-cli` · Bash 5+, GNU coreutils · Outcome: validate first, preserve an old output on failure, and make dry-run genuinely non-writing.

Prerequisites: [[08-bash-functions-scope]], [[09-bash-redirections]], [[12-bash-args-options]], [[14-set-shopt-strict-debug]], [[15-builtins-printf-read-exec-eval]].

## Contract

`bash main.sh [--dry-run] --output FILE [--] INPUT`

Number every input line, including blank lines, as `NUMBER<TAB>ORIGINAL<newline>`. Preserve whitespace, backslashes and a final unterminated line. Replace the output only after successfully generating the report. Repeated runs produce the same output.

Require a readable regular input and existing writable output parent. Reject symlink/non-regular outputs and input/output referring to the same file. This is a private training sandbox, not race-proof handling of attacker-controlled directories.

`--help` → stdout/`0`; misuse → stderr/`2`; I/O/safety failure → stderr/`1`. Successful writes produce no stdout. Dry-run prints a plan and creates/modifies **nothing**, including temporary files.

```bash
python3 90-tools/practice.py start bash-cli
python3 90-tools/practice.py check bash-cli
```

Completion: show a failing invocation leaves an existing report unchanged; explain same-filesystem rename versus crash durability and metadata preservation. Extend with a no-clobber option and regression tests.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/bash-cli/explanation.md) · [Bash builtins](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html)
