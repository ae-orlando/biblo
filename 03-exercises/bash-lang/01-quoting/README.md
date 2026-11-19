# Lab: preserve arbitrary filenames

**ID:** `bash-quoting` · Bash 5+, GNU find/sort · Outcome: preserve pathname boundaries through expansion and pipelines.

Prerequisites: [[01-shell-model]], [[03-quoting-splitting-globbing]], [[07-bash-loops]], [[09-bash-redirections]].

Implement `work/main.sh DIR`. Emit the basename of each immediate regular file, including hidden files but excluding directories and symlinks. Separate records with NUL bytes; order by byte value (`LC_ALL=C`). Never modify files. Empty directory → empty stdout/status `0`; wrong argument count → stderr/status `2`; missing/unreadable directory → stderr/status `1`.

The test creates names containing spaces, newline, quotes, `*`, and leading `-`. Newlines cannot be your record separator. Do not parse `ls`.

```bash
python3 90-tools/practice.py start bash-quoting
python3 90-tools/practice.py check bash-quoting
```

Tests invoke Bash explicitly; your interactive zsh settings are irrelevant. NUL output is binary-framed data, so an ordinary text editor or line count is not a validator.

Completion: explain which layer expands a glob and why `"$@"` differs from `$*`. Deliberately introduce unquoted splitting, catch it, then extend the task to recursive traversal with an explicit symlink policy.

[Hints](hints.md) · [Reference explanation](../../../07-solutions/bash-quoting/explanation.md) · [Bash expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html)
