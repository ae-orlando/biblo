---
created: 2026-10-08
updated: 2026-10-21
---

# 06 — Conditionals (`[[ ]]`, `(( ))`, `case`, `=~`)

> Prerequisites: expansion and quoting. Outcome: distinguish literal, glob, regex and arithmetic conditions. Practice: `bash-cli` in [[practice-catalog]]. Quoting a RHS pattern/regex changes semantics; “quote optional but harmless” is not a universal rule.

## Mental model

Three test commands: `[[ ]]` (bash, strings/files/patterns/regex — no splitting, quote optional but harmless), `[ ]` (POSIX, quote EVERYTHING, numbers only `-eq` family, `>` must be `\>`), `(( ))` (arithmetic, exit 0 iff nonzero, no `$` needed). Pick `[[ ]]` for strings/files, `(( ))` for numbers.

```bash
v="a b"
[[ $v == "a b" ]] && echo "[[ ]]: no split, fine unquoted"
[ "$v" = "a b" ] && echo "[ ]: MUST quote"
[ $v = foo ] 2>&1  # FAILS: unary operator expected (splits to 3 words)
i=5; (( i++ )); echo "$i"  # 6
(( 2+2 == 4 )) && echo "arith true"
```

## File / string / number tests
```bash
[[ -f f && -d /tmp && -L link && -e f && -r f && -w f && -s f ]]
[[ -z "" ]]; [[ -n "x" ]]
[[ -v HOME ]]; [[ ! -v NOPE ]]     # -v: is var set (bash 4.2+)
[[ -v 'arr[0]' ]]                  # -v works on array elements too
[[ "abc" < "abd" ]]                # lexicographic (< > inside [[ ]] need NO escape; locale-dependent)
[[ 3 -eq 3 && 3 -ne 4 && 3 -lt 5 && 3 -le 3 && 5 -gt 3 && 5 -ge 5 ]]
(( n >= 3 )) && echo big           # numbers cleaner in (())
# Full file primaries: -b -c -p -S (block/char/fifo/socket), -g -u -k (suid/sgid/sticky),
# -O (owned by you), -G (your group), -N (modified since read), -t fd (is a terminal)
[[ -t 1 ]] && echo "stdout is a tty"
[[ a -nt b ]] && echo "a newer than b"   # -nt/-ot mtime compare; -ef same inode (hardlink?)
[[ a -ef b ]] && echo "same file"
# Shell-option test: [[ -o pipefail ]] — is set -o option on?
# Grouping inside [[]]: [[ ( -f f && -r f ) || -d d ]] — () and ! && || work, no splitting
```

## Regex `=~` (right side UNQUOTED = ERE; quoted chunk = literal)
```bash
s="user-123-abc"
if [[ $s =~ ([a-z]+)-([0-9]+) ]]; then
  echo "${BASH_REMATCH[0]} ${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
fi  # user-123 user 123
[[ "123" =~ "([0-9]+)" ]] || echo "quoted = literal, no match"
re='^a[0-9]+$'; [[ a42 =~ $re ]] && echo "var-held regex: yes"
```

## `case` (globs, `|` alternation)
```bash
case $w in
  foo)     echo exact ;;
  [Bb]ar*) echo glob ;;
  *@*|*.*) echo alt ;;
  *)       echo default ;;
esac
# ;; stop | ;& run-next-blindly | ;;& re-test-next-pattern
shopt -s nocasematch; case FoO in foo) echo nocase;; esac; shopt -u nocasematch
```

## `if` / `&&` / `||` forms
```bash
if [[ -f f ]]; then echo file; elif (( n > 3 )); then echo big; else echo other; fi
[[ -f f ]] && echo exists || echo missing   # short-circuit; careful: a&&b||c runs c if b fails too
cmd && success || fail   # idiom for simple either/or only
```

## Pitfalls

- `[ $x == 3 ]` for numbers (SC2071) — `==` in `[ ]` is string compare; use `-eq` or `(( x == 3 ))`.
- `[[ a.txt == "*.txt" ]]` quoted RHS never matches as pattern — quote vars only when you want literal.
- `a && b || c` is NOT if/else — if `b` fails, `c` runs too. Use real `if` for 3-step logic.
- `(( 0 ))` under `set -e` exits the script — `(( x++ )) || true` for counters starting at 0. See [[14-set-shopt-strict-debug|14]].
- `[[ $a < $b ]]` sorts by locale — `LC_ALL=C` for byte order in scripts.

## Try it

```bash
bash -c 'v="a b"; [[ $v == "a b" ]] && echo ok1; [ "$v" = "a b" ] && echo ok2'
bash -c 's="user-123"; [[ $s =~ ([a-z]+)-([0-9]+) ]] && echo "${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"'
bash -c 'case Bar9 in [Bb]ar*) echo glob;; *) echo no;; esac'
bash -c '(( 0 )); echo "rc:$?"; (( 1 )); echo "rc:$?"'
mkdir -p .practice-runtime/scratch/conditions
bash -c 'd=.practice-runtime/scratch/conditions; touch -d "1 hour ago" "$d/old"; touch "$d/new"; [[ $d/new -nt $d/old ]] && echo newer-ok; [[ -t 1 ]] && echo tty || echo notty'
```

## Optional scratch drills (inside bash-cli/work)

1. `classify.sh`: arg = file/dir/link/missing/other using `[[ -f/-d/-L/-e ]]`; unquoted path with space must still work — prove quoting. Add `-nt/-ot` compare of two files.
2. `version.sh`: `[[ $1 =~ ^v?([0-9]+)\.([0-9]+) ]]` — print major/minor via `BASH_REMATCH`, else usage+exit 2. Show quoted-regex failure in a comment.
3. `grade.sh`: number arg → A/B/C/F with `(( ))` ranges; reject non-numbers (`[[ $1 =~ ^[0-9]+$ ]]` guard first).

## Related

- [[07-bash-loops|Loops]]
- [[04-bash-parameters|Parameters]]
- [[02-bash-expansions|Expansions]] (arithmetic table)
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]]

Sources: [Conditional constructs](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html), [conditional expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html). Gate: test invalid options and unsafe output paths without modifying an existing report.
