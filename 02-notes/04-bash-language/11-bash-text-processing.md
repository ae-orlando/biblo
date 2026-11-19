---
created: 2026-10-08
updated: 2026-10-21
---

# 11 — Text Processing (bridge: bash orchestrates, tools work)

> Prerequisites: redirections, quoting and process statuses. Outcome: choose record framing and propagate parser failures. Practice: `bash-pipeline` in [[practice-catalog]].

> Scope: grep, sed, awk, sort and cut are separate programs, not Bash syntax. They do not all come from GNU coreutils: GNU grep/sed/gawk are separate packages. Bash supplies arguments, redirections and process control.

## Mental model

Bash orchestrates; small text tools do the work. `rg` finds lines, `sed` edits streams, `awk` processes columns, `sort/uniq/cut` reshape. Prefer `rg` over `grep -r` (respects `.gitignore`, skips binary, `-n` line numbers). Use `awk` when columns/conditions appear; leave bash for Python when logic nests.
Bash-side rules: feed tools with `< file` / `< <()` (not `cat |`), capture with `mapfile`/`read -ra` (not `for x in $(cat)`), keep `PIPESTATUS` (see [[01-shell-model|01]] + [[14-set-shopt-strict-debug|14]]).

```bash
rg -n "pacman" /etc/pacman.conf
rg -n "ERROR" app.log | cut -d: -f1 | sort | uniq -c | sort -nr | head
mapfile -t hits < <(rg -l "TODO" --glob '*.sh' .)  # no pipe-subshell loss
```

## `sed` (stream edit — test WITHOUT `-i` first, it has no undo)
```bash
sed 's/foo/bar/g' file        # replace all per line (no g = first only)
sed -n '10,20p' file          # print lines 10-20 only (-n suppresses default print)
sed '/^#/d' file              # delete comment lines
sed -i.bak 's/a/b/g' file     # in-place WITH backup (then diff + rm .bak)
```

## `awk` (pattern-action per line; `$1..$NF` fields, `NR` lineno, `FS/OFS` separators)
```bash
awk '{print $1}' file              # first column
awk -F: '{print $1}' /etc/passwd   # custom separator
awk '$3 > 1000 {print $1}' file     # condition + action
awk '{s+=$2} END {print s}' nums    # sum column 2 (END runs once)
df -h | awk '$5+0 > 80 {print $0}'  # disks over 80% ($5 like 82% → +0 numeric)
```

## Reshape set
```bash
sort file | uniq -c | sort -nr | head   # top duplicates (uniq needs SORTED input)
sort -t: -k3 -n /etc/passwd             # sort by 3rd :-field numerically
cut -d: -f1,7 /etc/passwd               # fields 1 and 7
tr a-z A-Z < file                       # translate chars
wc -l file; grep -c pattern file        # count lines / matches
paste -d, a.txt b.txt                   # join lines side by side
```

## Pitfalls

- uniq combines adjacent equal records only; sort first when you need global duplicate grouping and reordering is appropriate.
- `sed -i` without backup on a bad regex destroys the file — always `-i.bak` first run.
- `awk '$5 > 80'` on `82%` compares STRINGS — use `$5+0 > 80` to force numeric.
- `grep -r` on binary dirs garbles terminal — `rg` handles it; with grep add `-I`.

## Try it

```bash
printf 'b\na\nb\nc\n' | sort | uniq -c | sort -nr
printf 'u1:x:1001:a\nroot:x:0:b\n' | awk -F: '$3 > 100 {print $1}'
printf '82%%\n9%%\n' | awk '$1+0 > 80 {print "FULL:", $0}'
rg -n "Phase" ~/Documents/Notes/01-roadmap/master-plan.md | head -3
```

## Optional scratch drills (inside bash-pipeline/work)

1. `top-errors.sh`: from a log file, print top 5 `ERROR <code>` codes with counts (`rg/cut/sort/uniq/sort/head`).
2. `disks.sh`: `df -h` → `awk` lines with use% > 50 printing `mount: pct`; explain the `+0` in a comment.
3. `rename.sh`: `sed` preview (no `-i`) replacing a version string across `*.txt` copies, then `-i.bak` apply + `diff` proof.

## Related

- [[07-bash-loops|Loops]] (`while read` + tool pipelines)
- [[09-bash-redirections|Redirections]]

Sources: [GNU awk manual](https://www.gnu.org/software/gawk/manual/), [GNU sed manual](https://www.gnu.org/software/sed/manual/), [GNU coreutils](https://www.gnu.org/software/coreutils/manual/). Gate: detect a malformed late log record without emitting a partial success summary; explain the parser's status through a pipeline.
