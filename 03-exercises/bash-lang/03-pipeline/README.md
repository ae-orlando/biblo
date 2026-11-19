# Lab: validate a log stream before emitting a summary

**ID:** `bash-pipeline` · Bash 5+, awk · Outcome: make pipeline failure and output contracts explicit.

Prerequisites: [[09-bash-redirections]], [[11-bash-text-processing]], [[14-set-shopt-strict-debug]].

Implement `work/main.sh LOG`. Each input line begins `LEVEL<TAB>message`, where level is exactly ERROR, INFO or WARN and the first message field is nonempty. Additional tab-separated message fields are allowed. Invalid records must produce stderr/nonzero status and **no partial summary**.

Valid output is exactly three tab-separated rows, in order: ERROR count, INFO count, WARN count. Empty input produces three zero counts. Wrong argument count → `2`; unreadable/missing file → `1`. Do not modify input.

Example: two INFO lines and one ERROR produce `ERROR<TAB>1`, `INFO<TAB>2`, `WARN<TAB>0`.

```bash
python3 90-tools/practice.py start bash-pipeline
python3 90-tools/practice.py check bash-pipeline
```

Completion: explain why a successful final `sort` does not prove an earlier parser succeeded. Introduce a malformed late record and prove no success output leaks. Extend the parser to accept a documented timestamp field; preserve diagnostics and framing.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/bash-pipeline/explanation.md) · [GNU awk manual](https://www.gnu.org/software/gawk/manual/)
