---
created: 2026-10-08
updated: 2026-10-21
---

# 15 — Builtins: `printf`, `read`, `exec`, `eval`, `source`

> Prerequisites: quoting, loops and redirections. Outcome: preserve text, avoid format-string injection and distinguish loading code from passing data. Practice: `bash-cli` and `bash-jobs` in [[practice-catalog]].

## Mental model

Builtins manipulate the shell itself — no fork, they see/alter locals, fds, and positionals. External tools (`awk/sed`) transform text; builtins wire it up. Master five: `printf` (output), `read/mapfile` (input), `exec` (fds/process), `source` (load lib), `eval` (re-parse — last resort).

## `printf` (use INSTEAD of `echo` for anything non-trivial)
```bash
printf '%s,%s\n' a b             # format reuse: extra args repeat the format
printf '%d %5s %-5s|\n' 42 hi hi # 42    hi hi   | — width/align
printf '%q\n' 'a b"c$d'         # a\ b\"c\$d — re-eval-safe (pairs with eval, see below)
printf -v out '%s=%d' x 5; echo "$out"  # -v VAR: no subshell, no trailing-newline loss
printf '%(%F)T\n' -1            # 2026-10-08 — strftime on epoch (-1 = now)
printf '%s\n' "${arr[@]}" >f    # join array to file (one per line)
# echo pitfalls: echo -n/-e vary by xpg_echo; printf is POSIX-stable. ShellCheck SC2059: don't printf "$var" (use %s).
```

## `read` + `mapfile` (the only correct input idioms)
```bash
IFS= read -r line <file            # ONE line, edge spaces + backslashes preserved
while IFS= read -r line || [[ -n $line ]]; do echo "L:$line"; done <file  # catches missing trailing newline
IFS=: read -r user _ _ _ _ home shell < /etc/passwd  # _ throwaways; IFS=: splits on colon
read -ra arr <<< "a b  c"          # -a array; IFS controls split
read -p "Name? " -r name           # -p prompt (stderr); combine with -r always
read -t 5 -r ans || echo timeout   # -t seconds (0.1 works); rc!=0 on timeout/EOF
read -s -r secret <<< "pw"         # -s silent (no echo); -n1 one char; -d '' NUL-delim
read -u 3 -r x 3< f                # -u FD: read from fd 3
printf 'a\0b\0' | mapfile -d '' -t nz  # NUL list (pairs with find -print0)
```

## `exec`, `source`, `command`, `builtin`
```bash
exec 3>fd.log; echo via >&3; exec 3>&-      # exec = permanent fd redirect (no fork)
exec >all.log 2>&1                          # redirect REST of script
exec cmd args                               # REPLACE process (last line of wrappers; no return)
source lib.sh; . lib.sh                     # both load in Bash; POSIX standardizes dot, not source
[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"  # source-guard (see note 08)
command ls ...                              # bypass alias/function
builtin echo hi                             # force builtin
```

## `eval` (re-parse — quote with `%q`/`@Q` or don't use it)
```bash
cmd='ls -l "$HOME"'; eval "$cmd"            # re-parses string as code (word-split/expand AGAIN)
v='a b"c'; eval "echo $(printf '%q' "$v")"  # SAFE pattern: %q-encode before eval
# Prefer: arrays + "${cmd[@]}" (no eval), declare -n namerefs (no eval), case dispatch (no eval).
# NEVER: eval "$user_input" / eval "cmd $unquoted" — injection. ShellCheck SC2089/SC2090.
```

## `:` / `true` / `false`, `type`, `declare`
```bash
: "${DATA_DIR:=$HOME/data}"     # : no-op — evaluates args (assigns defaults), rc 0
: > truncate.txt                # truncate idiom
true; echo $?; false; echo $?   # 0 / 1 — loop conditions, stubs
type -a printf; command -v awk  # what WOULD run (all matches vs first path)
declare -p var arr m            # inspect (re-assignable output); declare -F (func names), -f (bodies)
export -f myfunc                # export FUNCTION to child bash; unset -f myfunc removes
caller; echo "${FUNCNAME[*]}"   # stack in debug paths
```

## Pitfalls

- `echo $var` with `-n`/`-e` inside data — `printf '%s\n' "$var"`.
- `read` without `-r` mangles `\`; without `IFS=` strips indent. Config readers need both.
- `cmd | read x` — `read` in subshell, `x` lost. Use `< <(cmd)` or `lastpipe`.
- `eval` on unquoted vars double-splits AND globs. Encode first or use arrays.
- `exec cmd` never returns — anything after it is dead code unless `exec` fails.

## Try it

```bash
bash -c 'printf "%q\n" "a b\"c"; printf -v q "%q" "a b"; echo "v=$q"; printf "%(%F)T\n" -1'
bash -c 'printf "  a  \nb\\\\c\n" | { while IFS= read -r l; do printf "<%s>\n" "$l"; done; }'
bash -c 'v="a b"; e=$(printf "%q" "$v"); eval "echo E:$e"; declare -p v e'
bash -c 'f(){ caller; }; f; type -a ls | head -2; command -v bash'
```

## Optional scratch drills (inside bash-cli/work)

1. `printf.sh`: table with `%5s/%-5s/%d/%q`, `-v` capture, `%(%F)T` date. Show `echo -e` vs `printf` on a string containing `-n`.
2. `readall.sh`: preserve whitespace/backslashes and a final unterminated line. Compare simple IFS comma splitting with real quoted CSV: read -a is not a general CSV parser; use a dedicated parser for quoted fields/newlines.
3. `noeval.sh`: take `cmd='ls -l "$HOME"'` — run via array (no eval), then via `%q`+`eval` with a space-in-filename proof that naive `eval $cmd` breaks.

## Related

- [[04-bash-parameters|Parameters]] (`${var@Q}`, `declare -p`)
- [[05-bash-arrays|Arrays]] (`read -a`, `mapfile`)
- [[07-bash-loops|Loops]] (`while read`, `< <()`)
- [[08-bash-functions-scope|Functions]] (source-guard, `export -f`)

Sources: [Bash builtins](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html), [Bourne shell builtins](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html). Gate: explain why an array invocation avoids reparsing and why printf '%s' differs from printf "$data". Bash quoting is not universal encoding for other languages.
