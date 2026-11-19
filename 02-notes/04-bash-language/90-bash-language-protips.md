---
created: 2026-10-08
updated: 2026-10-21
---

# Bash Language Protips

> **Editor qualification, 2026-10-21; history preserved.** Pre-increment can still return false when it produces zero; use explicit arithmetic assignment when its status is not a condition. Line-reading does not preserve arbitrary newline-containing filenames; use NUL framing. Bash quoting is not a universal encoder for remote shells or other languages. Test current behavior rather than treating a gotcha line as a complete specification.

Living list for LANGUAGE gotchas (quoting/expansion/scope — automation tips go in scripting track's `90-bash-protips.md`). Append-only, newest on top. Tag each entry `[01]`–`[16]` for the note it belongs to.

How to add:
```md
## YYYY-MM-DD — short title [NN]
Context: what you were doing
Run: `exact command`
Why: one line
```

---

## 2026-10-08 — `PIPESTATUS` went stale [01/14]
Context: checked `"${PIPESTATUS[0]}"` after an `echo`.
Run: `cmd | tee log; ps=("${PIPESTATUS[@]}")` immediately
Why: any command overwrites it — save first.

## 2026-10-08 — `"$*"` collapsed args [01]
Context: `for f in "$*"` joined `"a b" "c"` into one.
Run: `for f in "$@"`
Why: `"$@"` = one word per arg; `"$*"` = one word joined by IFS.

## 2026-10-08 — `eval` double-split a path [15]
Context: `eval "cmd $file"` broke on spaces.
Run: `cmd=("./run" "$file"); "${cmd[@]}"` (no eval) or `eval "cmd $(printf '%q' "$file")"`
Why: eval re-splits+globs; arrays don't.

## 2026-10-08 — Empty array aborted under `set -u` [05/14]
Context: `"${arr[@]}"` on empty array with `set -u` (bash <4.4).
Run: `${arr[@]:-}` guard or upgrade bash
Why: nounset treats empty expansion as unbound on old bash.

## 2026-10-08 — Stored `~/x` in a var, tool not found [02]
Context: `p='~/bin'; $p/tool` failed.
Run: `p="$HOME/bin"; "$p/tool"`
Why: tilde-after-param never expands (expansion order: tilde before param).

## 2026-10-08 — Brace range from a variable didn't expand [02]
Context: `s='{1..3}'; echo $s` printed literally.
Run: `echo {1..3}` (or `seq`/`for ((i..))` for dynamic ranges)
Why: brace runs FIRST; param results are never rescanned for it.

## 2026-10-08 — Counter killed script under `set -e` [02/14]
Context: `((i++))` with `i=0` aborted installer.
Run: `((++i)) || true`
Why: `(( ))` exits 1 when value is 0; pre-increment (or `|| true`) avoids it.

## 2026-10-08 — `local` hid a real failure [08]
Context: function always "succeeded".
Run: `local out; out=$(cmd)` (two lines)
Why: `local x=$(...)` returns 0 regardless (SC2155).

## 2026-10-08 — Merge redirections in the wrong order [09]
Context: log file missing stderr.
Run: `cmd >f 2>&1` (not `2>&1 >f`)
Why: target first, dup second — reversed sends stderr to the OLD stdout.

## 2026-10-08 — `${v: -2}` needs the space [04]
Context: `${v:-2}` returned default instead of slice.
Run: `${v: -2}` / `${v:1:-1}`
Why: no space parses as `:-` default operator.

## 2026-10-08 — Quoted regex never matched [06]
Context: `[[ $x =~ "([0-9]+)" ]]` always false.
Run: `[[ $x =~ ([0-9]+) ]]` or `re='...'; [[ $x =~ $re ]]`
Why: quoted regex chunks are literal.

## 2026-10-08 — `for f in $(ls)` broke on spaces [03/07]
Context: filenames with spaces split.
Run: `for f in *` / `while IFS= read -r`
Why: command substitution results split+glob; globs don't.

---

## Related

- [[00-how-to-use-track|How to Use This Track]]
- [[02-bash-expansions|Expansions]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]]
- [[15-builtins-printf-read-exec-eval|Builtins]]
- [[16-shell-vars-index|Shell Variables Index]]
- [[90-bash-protips|Bash Protips]] (scripting track)
