---
created: 2026-10-08
updated: 2026-10-21
---

# 02 — Expansions (the order model)

> Prerequisite: [[01-shell-model]]. Outcome: predict words before a command sees them. Practice: `bash-quoting`, then `bash-capstone`, in [[practice-catalog]]. Arithmetic is not a safe parser for untrusted expressions and has finite integer range.

## Mental model

One line goes through this pipeline, in order (from `man bash` EXPANSION). Memorize it — every "weird" bash behavior is just this order:

1. **Brace** `{a,b}`, `{1..5}` (textual, first)
2. **Tilde** `~/x`, `~user`
3. **Parameter/variable** `$v`, `${v}`, **command** `$( )`, **arithmetic** `$(( ))`, **process** `<( )` (left-to-right together)
4. **Word splitting** (unquoted results only, on `IFS`)
5. **Pathname expansion** (globbing `* ? [...]`, unquoted only)
6. **Quote removal** (last — quotes did their job, now stripped)

Brace expansion, splitting and globbing can increase word count. Quoted "$@" and "${array[@]}" are important special cases that also preserve multiple words. Predict these examples, then compare with the actual Bash runtime:
```bash
s='{1..3}'; echo "$s" "$s"  # {1..3} — param result is NOT rescanned for brace
a='~/x'; echo "$a"          # ~/x — tilde-after-param does NOT expand
v=x; echo {$v,'$v'}         # x $v — brace first, then param inside
FOO=~/bar; echo "$FOO"      # /home/... — tilde DOES expand in assignments
```

## Brace expansion (textual, needs unquoted `{` + `,` or valid range)
```bash
echo {a,b,c}        # a b c
echo {1..5}         # 1 2 3 4 5
echo {01..10}       # 01 02 ... 10 (zero-padded, equal width)
echo {1..10..2}     # 1 3 5 7 9 (step)
echo {5..1}         # 5 4 3 2 1
echo a{d,c,b}e      # ade ace abe (left-to-right, NOT sorted)
echo {a,b{1,2},c}   # a b1 b2 c (nested)
echo {a..c}{1..2}   # a1 a2 b1 b2 c1 c2 (cartesian)
echo "{a,b}" {a}    # literal — quoted / no comma = no expansion
mkdir -p proj/{src,tests,docs}   # canonical use
```
Disable brace expansion with `set +B` or `set +o braceexpand`; there is no `nobraceexpand` option name.

## Tilde (only word-initial, unquoted `~`; result is quoted = no split/glob)
```bash
echo ~ ~/x ~root ~+ ~-   # HOME, HOME/x, root's home, PWD, OLDPWD
PATH=/x:~/y              # expands after = and : in assignments
```

## Command + arithmetic substitution
```bash
echo "today $(date +%F) files: $(ls | wc -l)"
echo $((2 + 3 * 4)) $((2**10)) $((5/2)) $((16#ff))  # 14 1024 2 255
i=5; echo $((i++)) $i   # 5 6 — $ optional inside (())
(( i += 2 )); echo $i   # 8 — (()) runs arithmetic as a COMMAND (exit 0 iff nonzero)
```
`$( )` starts a **new quoting context** — quote inside independently: `"a $(b "$c")"`.
Command substitution **strips ALL trailing newlines**: `b=$(printf 'x\n\n'); echo "${#b}"` → `1`. Legacy `` ` ` `` backticks nest poorly — always `$( )`.

## Arithmetic: full operator table (C-like, integers only)
```bash
echo $((16#ff)) $((8#17)) $((2#101)) $((64#10))  # 255 15 5 64 — base#n, base 2-64
echo $(( 5 + 3 * 2 % 4 ))           # 7 — precedence: ** then * / % then + -
echo $(( 2**10 )) $(( 1<<3 )) $(( 16>>2 ))  # 1024 8 4
echo $(( 5 & 3 )) $(( 5 | 2 )) $(( 5 ^ 1 )) $(( ~5 ))  # 1 7 4 -6 (two's complement)
echo $(( 5 > 3 ? 10 : 20 ))         # 10 — ternary
echo $(( (1, 2, 3) ))               # 3 — comma: value is LAST
i=0; (( ++i )); echo "$i $?"        # 1 0 here; incrementing -1 to 0 still returns false
(( v = 5 > 3 ? 10 : 20 )); echo "$v"  # 10 — assignment inside (())
declare -i iv; iv="3 + 4 * 2"; echo "$iv"  # 11 — arithmetic on assignment
let "x = 2 + 3"; echo "$x"          # 5 — legacy alternate to (( x = 2 + 3 ))
```
Arithmetic variable names normally need no dollar sign: `$((i++))` increments i. It is **not** equivalent to `$(( $i++ ))`, which can expand into invalid text such as `5++`. Unset names often evaluate to zero unless nounset changes the behavior; divide by zero errors, integers overflow, and no floating-point arithmetic is provided. Validate input before evaluation; recursive arithmetic evaluation can interpret names/expressions you did not intend.

## Arch note

Nothing Arch-specific — this is pure `man bash` `/^EXPANSION/` + ARITHMETIC EVALUATION. Read those sections once after this note; they will now make sense.

## Pitfalls

- `echo $s` where `s='{1..3}'` expecting `1 2 3` — brace already passed. Generate ranges unquoted at write-time.
- `p='~/bin'; $p/tool` fails — tilde stored, never expanded. Store `$HOME/bin`.
- `(( 0 ))` exits 1 (zero = false) — under `set -e` it kills the script. Guard: `(( x++ )) || true`.
- Expecting floats: `$(( 5/2 ))` is `2`. Use `awk 'BEGIN{print 5/2}'`.
- `let "x = 2"` with spaces needs quotes; prefer `(( x = 2 ))`.

## Try it

```bash
bash -c 's="{1..3}"; echo "$s"; echo {1..3}'
bash -c 'v=x; echo {$v,'\''$v'\''}'
bash -c 'echo $((2**10)) $((16#ff)) $((5/2))'
bash -c 'i=0; (( i++ )); echo "rc:$? i:$i"'
bash -c 'echo $((16#ff)) $((8#17)) $((2#101)) $(( 5 > 3 ? 10 : 20 )) $(( (1,2,3) ))'
bash -c 'b=$(printf "x\n\n"); echo "${#b}"; declare -i iv; iv="3+4*2"; echo "$iv"'
```

## Optional scratch drills (inside bash-quoting/work)

1. `brace.sh`: one `mkdir -p` creating `proj/{src,tests,docs}` + `touch proj/{src,tests}/keep.md`. Then prove `p='proj/{src,tests}'; ls $p` fails and explain why in a comment.
2. `order.sh`: predict then run: `a='~/x'; echo $a`, `v=y; echo {$v,$v}`, `echo {1..6..2}`. Comment each with the pipeline step responsible.
3. `arith.sh`: print `2**10`, `16#ff`, `5/2`, `5%2`; show `(( 0 )); echo $?` vs `(( 1 )); echo $?`. Add: ternary `5>3?10:20`, bases `8#17`/`2#101`, pre-incr safety `((++i))` under `set -e`.

## Related

- [[01-shell-model|Shell Model]]
- [[03-quoting-splitting-globbing|Quoting, Splitting, Globbing]]
- [[06-bash-conditionals|Conditionals]] (`(( ))` as test)
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]]

Sources: [Shell expansions](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html), [shell arithmetic](https://www.gnu.org/software/bash/manual/html_node/Shell-Arithmetic.html). Gate: predict splitting/globbing effects on the filename lab, then explain a deliberately caught quoting bug. Execution scope: [[implementation-status]].
