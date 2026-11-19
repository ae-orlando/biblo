---
created: 2026-10-08
updated: 2026-10-21
---

# 09 — Redirections (fds, heredocs, process substitution)

> Prerequisite: [[01-shell-model]]. Outcome: predict stream destinations and avoid clobbering output before validation. Practice: `bash-cli` and `bash-pipeline` in [[practice-catalog]].

## Mental model

Every process has fds: 0 stdin, 1 stdout, 2 stderr. Redirection rebinds them. **Order matters**: `>f 2>&1` (stdout→file, stderr→same) vs `2>&1 >f` (stderr→OLD stdout, stdout→file — usually wrong). `tee` duplicates a stream. `<( )` turns a command's output into a *filename*.

```bash
./a >out.txt 2>err.txt   # split
./a >all.txt 2>&1        # merge into one (ORDER: file first, then dup)
./a &>both.txt            # bash short for >both 2>&1; &>> appends both
./a |& cat               # == 2>&1 | — pipe BOTH to next command
echo hi | tee copy.txt | tr a-z A-Z   # screen/file split; tee -a appends
```

## Stdin sources
```bash
cat < out.txt            # file as stdin
grep foo <<< "foobar"    # herestring (adds trailing newline)
cat <<EOF                # heredoc — EXPANDS $vars and $( )
expanded $HOME $(echo x)
EOF
cat <<-E2                # <<- strips leading TABS only (not spaces)
	E2
cat <<"EOF3"             # quoted delimiter — NO expansion (use for code templates)
literal $HOME $(echo no)
EOF3
```

## fd juggling + process substitution
```bash
./a 3>&1 1>out.txt 2>err.txt  # keep original stdout on fd 3 while splitting
exec 3>fd3.txt; echo via >&3; exec 3>&-       # persistent fd, then close
exec {myfd}>auto.txt; echo data >&$myfd; exec {myfd}>&-  # auto fd number (>=10)
exec >all.log 2>&1          # persistent redirect for REST of script (use in main)
diff <(printf 'a\nb\n') <(printf 'a\nc\n') || true
cmd > >(tee install.log)   # process sub as a redirect TARGET
# coproc: two-way pipe (rare — <()/$() covers 95%): coproc C { cat; }; echo hi >&"${C[1]}"
```

## Extras (know they exist)
```bash
echo hi >| clobber.txt      # >| overrides set -o noclobber once
: > truncate.txt            # : no-op + > truncates/creates
exec 3<> rw.txt             # <> read+write without truncating
cmd <&- 3>&-                # close stdin / fd 3
# /dev/stdin, /dev/stdout and /dev/stderr refer to descriptors; do not blindly
# read your own output descriptors. /dev/null discards; Bash has network redirs.
# NOTE: ./a &>both.txt is bash-only (not POSIX sh). Portable merge: ./a >both.txt 2>&1
```

## Pitfalls

- `2>&1 >f` when you meant merge — memorize `>f 2>&1` (target first, dup second).
- `> file` with `set -o noclobber` refuses to clobber — override once with `>| file`.
- Heredoc indented with spaces + `<<-` still keeps them — `<<-` strips TABS only.
- Unquoted heredoc runs command substitutions — secrets/commands execute on write. Quote the delimiter for templates.

## Try it

```bash
bash -c 'diff <(printf "a\nb\n") <(printf "a\nc\n") || echo "rc:$?"'
mkdir -p .practice-runtime/scratch
bash -c 'printf "hello\n" | tee .practice-runtime/scratch/tee.txt | tr a-z A-Z; cat .practice-runtime/scratch/tee.txt'
bash -c 'cat <<EOF
$HOME $(echo inner)
EOF'
bash -c 'cat <<"EOF"
$HOME $(echo inner)
EOF'
```

## Optional scratch drills (inside bash-cli/work)

1. `merge.sh`: script writing to stdout+stderr; demonstrate `>f 2>&1` (merged) vs `2>&1 >f` (split) with `cat` proof of each file.
2. `template.sh`: heredoc generating a config with `$HOST` expanded in one block and literal `$HOME` preserved in another (quoted delimiter).
3. `fd.sh`: `diff <(sort a.txt) <(sort b.txt)` on two small files + `tee` pipeline saving mid-pipe output to a log.

## Related

- [[07-bash-loops|Loops]] (loop input via `< file` / `< <()`)
- [[10-bash-traps-jobs|Traps & Jobs]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]] (`noclobber`, `BASH_XTRACEFD`)
- [[15-builtins-printf-read-exec-eval|Builtins]] (`exec`, `/dev/*`)

Sources: [Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html). Gate: explain why redirection may create/truncate a file before the command runs and prove dry-run creates no temp/output file in the CLI lab.
