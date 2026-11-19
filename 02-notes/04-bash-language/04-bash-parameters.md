---
created: 2026-10-08
updated: 2026-10-21
---

# 04 — Parameters (the full `${}` family)

> Prerequisite: [[03-quoting-splitting-globbing]]. Outcome: distinguish missing/empty defaults and glob-based string operations. Practice: `bash-cli` and `bash-capstone` in [[practice-catalog]].

## Mental model

Parameter expansion includes defaults, errors, lengths, slices, pattern removal/replacement and case changes. Patterns here are globs, not regex. The examples are reference material; see [[implementation-status]] for the narrower executed verification record.

## Defaults and errors (`:` = also treat empty as unset)

```bash
unset u; e=""
echo "[${u:-d}][${e:-d}]"   # [d][d] — default if unset OR null
echo "[${u-d}][${e-d}]"     # [d][]  — no colon: only if unset
echo "${u:=hi}"; echo "$u"  # hi / hi — ASSIGNS default
: "${DATA_DIR:=$HOME/data}" # canonical "set default" line
v=x; echo "[${v:+alt}]"     # [alt] — alt if set AND non-empty
bash -c 'unset u; echo ${u:?need it}'; echo $?  # bash: u: need it, rc=1
```
`${v?msg}` (no colon) passes empty. Use `:?` to assert required vars at script top.

## Length and slices
```bash
v=hello; echo "${#v} ${v:1:3} ${v:1}"  # 5 ell ello (0-indexed)
echo "${v: -2} ${v:1:-1}"             # lo ell — SPACE before negative offset is mandatory
```

## Strip from front/back (glob; shortest vs longest)
```bash
p=a-b-c; echo "${p#*-} ${p##*-} ${p%-*} ${p%%-*}"  # b-c c a-b a
f=/path/to/archive.tar.gz
echo "${f##*/}"  # archive.tar.gz — basename idiom
echo "${f%/*}"   # /path/to — dirname idiom
echo "${f##*.}"  # gz — extension
echo "${f%.*}"   # /path/to/archive.tar — strip ext
s=${f##*/}; echo "${s%.*}"  # archive.tar — stem
```

## Replace (first / all; `#` prefix / `%` suffix anchors)
```bash
v=/aa/bb/aa; echo "${v/aa/XX} ${v//aa/XX}"    # /XX/bb/aa /XX/bb/XX
echo "${v/#\/aa/X} ${v/%aa/X}"               # X/bb/aa /aa/bb/X
v=aaa; echo "[${v/a/}] [${v//a/}]"            # [aa] [] — empty replacement deletes
```

## Case change (bash 4+)
```bash
v=hello; echo "${v^} ${v^^} ${v,} ${v,,}"  # Hello HELLO hello hello
```

## Transforms `${var@op}` (bash 4.4+, quoting/serialization)
```bash
v='a b"c$d'; echo "${v@Q}"   # 'a b"c$d' — quoted, re-eval-safe (use in logs/declare -p round-trips)
echo "${v@E}"                # expands \n \t etc. (reverse of $'...')
w=hello; echo "${w@U} ${w@L}"  # HELLO hello — upper/lower (alternate to ^^/,,)
declare -p v                 # declare -- v='a b"c$d' — canonical inspect
declare -A m=([k]="v v"); declare -p m  # declare associative type explicitly
# ${m@K} provides quoted key/value information; ${m@A} is assignment-style output.
printf '%q\n' "$v"           # a\ b\"c\$d — same idea as @Q but as printf (see note 15)
```
Prefer arrays/direct arguments to reparsed strings. @Q and printf %q quote for compatible Bash syntax; they are not universal encoders for remote shells, SQL, JSON or every nested quoting layer. Avoid eval when a direct representation works.

## Names and indirection
```bash
foo_bar=1; foo_baz=2; echo "${!foo_*}"    # foo_bar foo_baz — names with prefix
echo "${!foo_@}"                         # same but QUOTED list (safe with spaces/globs) — prefer @ over *
name=v; v=hello; echo "${!name}"          # hello — indirection
declare -n ref=v; echo "$ref"             # modern alternative to ${!}
```

## Variables: declare/local/readonly/export
```bash
declare -i iv; iv=3+4; echo "$iv"   # 7 — arithmetic on assignment
readonly RO=1; RO=2                 # bash: RO: readonly variable
export E=hi; bash -c 'echo $E'      # only exported vars reach children
```

## Pitfalls

- `${v: -2}` without the space parses as `${v:-2}` (default!). Always the space.
- Strip/replace patterns are globs — `*` not `.*`, no regex groups. For regex use `[[ =~ ]]`. With `shopt -s extglob` you get `+()/!()` here too.
- `readonly`/`-r` in functions without `local` leaks globally — `local -r x`.
- `${!prefix*}` unquoted re-splits names with IFS weirdness — use `${!prefix@}` quoted.
- macOS bash 3.2: no `^/,,/@Q`. Use `tr` / `printf %q` fallback.

## Try it

```bash
bash -c 'unset u; e=""; echo "[${u:-d}][${e:-d}][${u-d}][${e-d}]"'
bash -c 'f=/path/to/a.tar.gz; echo "${f##*/} ${f%.*} ${f##*.}"'
bash -c 'v=hello; echo "${v^} ${v^^} ${v:1:3} ${#v}"'
bash -c "v='a b\"c'; echo \"\${v@Q}\"; printf '%q\n' \"\$v\"; declare -p v"
```

## Optional scratch drills (inside bash-cli/work)

1. `path.sh`: given `/home/o/docs/a.tar.gz`, print basename, dirname, extension, stem using only `${}`.
2. `defaults.sh`: script taking `$1` optional with `${1:-world}`; assert required `$2` with `:?`; show `:-` vs `-` difference with empty string.
3. `replace.sh`: `v=/aa/bb/aa` — first/all/prefix/suffix replacements + uppercase whole string. Add: `extglob` replace `+([a-z])` and `@Q` dump of a value with spaces/quotes.

## Related

- [[05-bash-arrays|Arrays]]
- [[06-bash-conditionals|Conditionals]]
- [[15-builtins-printf-read-exec-eval|Builtins]] (`printf %q`, `declare -p`)

Sources: [Parameter expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html). Gate: explain the lab's missing-versus-empty argument policy and basename/extension handling, then test a boundary case.
