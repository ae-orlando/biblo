---
created: 2026-10-08
updated: 2026-10-21
---

# 07 — Loops (`for`, `while`, `until`, `select`)

> Prerequisites: arrays and conditionals. Outcome: preserve input records and reason about loop/subshell state. Practice: `bash-cli` and `bash-capstone` in [[practice-catalog]].

## Mental model

`for` iterates words/lists, C-style `for ((;;))` counts, `while` runs while exit==0, `until` runs while exit!=0, `select` builds menus. `break N`/`continue N` take a level (default 1). Files are read with `while IFS= read -r` — never `for x in $(cat)`.

```bash
for x in a b c; do echo -n "$x "; done; echo          # list (no `in` = `in "$@"`)
for ((i=0; i<3; i++)); do echo -n "$i "; done; echo   # C-style
i=0; while (( i < 2 )); do echo -n "w$i "; ((i++)) || true; done; echo
i=0; until (( i >= 2 )); do echo -n "u$i "; ((i++)) || true; done; echo
```

## Nested control
```bash
for i in 1 2 3; do
  for j in 1 2 3; do
    (( j == 2 )) && continue 2   # skip whole outer round when j==2
    echo -n "$i$j "
  done
done  # 11 21 31
```

## Reading line-oriented text (choose framing deliberately)
```bash
while IFS= read -r line; do printf '<%s>\n' "$line"; done < file
# IFS= keeps edge spaces, -r keeps backslashes
while IFS= read -r line || [[ -n $line ]]; do printf '%s\n' "$line"; done < file
# || [[ -n ]] catches a final line missing its newline
while IFS=: read -r user _ _ _ _ home shell; do echo "$user: $shell"; done < /etc/passwd
# _ = throwaway fields
count=0; while read -r l; do ((count++)) || true; done < <(printf 'a\nb\nc\n'); echo "$count"
# < <(...) NOT pipe — pipe puts the loop in a subshell, count would be lost
```

## `select` menus
```bash
select opt in apple banana quit; do echo "picked:$opt REPLY=$REPLY"; break; done <<< "2"
# menu on stderr, PS3 prompt, choice in $opt, raw input in $REPLY
```

## Pitfalls

- `for f in $(ls)` / `cat file | while read` — splitting/globbing + subshell var loss. Use globs and redirects.
- `((i++))` with `i=0` under `set -e` exits (result 0 = false). Write `((++i))` or `((i++)) || true`.
- `while read` without `-r` eats backslashes; without `IFS=` strips indentation — config files need both.
- `break` inside `case`/`select` counts `select` as a loop level — use `break 2` deliberately.

## Try it

```bash
bash -c 'for ((i=0;i<3;i++)); do echo -n "$i "; done; echo'
bash -c 'printf "  a  \nb\\\\c\n" | { while IFS= read -r l; do printf "<%s>\n" "$l"; done; }'
bash -c 'count=0; while read -r l; do ((++count)); done < <(printf "a\nb\nc\n"); echo "$count"'
```

## Optional scratch drills (inside bash-cli/work)

1. `lines.sh`: number every line of a file (`printf '%4d: %s\n'`), preserving spaces/backslashes and final-newline-less lines.
2. `passwd.sh`: parse `/etc/passwd` with `IFS=:` printing `user -> shell` for shells ending in `sh`.
3. `menu.sh`: `select` loop over `backup/restore/quit` with `PS3`, `REPLY` echo, `break` on quit, re-prompt on invalid.

## Related

- [[06-bash-conditionals|Conditionals]]
- [[05-bash-arrays|Arrays]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]] (`lastpipe`, `set -e` + `((i++))`)
- [[15-builtins-printf-read-exec-eval|Builtins]] (`read` flags, `mapfile -d`)

Sources: [Looping constructs](https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs.html), [BashFAQ/001](https://mywiki.wooledge.org/BashFAQ/001). Gate: preserve blank lines, backslashes and a final unterminated line in the CLI lab. Arbitrary filenames require NUL framing, not this line-reading contract.
