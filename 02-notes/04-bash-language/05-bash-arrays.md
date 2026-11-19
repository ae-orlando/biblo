---
created: 2026-10-08
updated: 2026-10-21
---

# 05 — Arrays (indexed, assoc, mapfile)

> Prerequisite: [[04-bash-parameters]]. Outcome: preserve lists without rebuilding them from strings. Practice: `bash-capstone` in [[practice-catalog]]; GNU/Linux and Bash 5+ are explicit lab requirements.

## Mental model

Indexed arrays hold ordered elements; associative arrays map keys to values. Quoted "${a[@]}" preserves each element as a separate argument. Quoted "${a[*]}" joins them into one string; unquoted forms can split/glob again. Unsetting an indexed element leaves a hole. Associative iteration order must not define output order.

## Indexed
```bash
a=(); a+=(x y "z w"); declare -p a   # a=([0]=x [1]=y [2]="z w")
printf '<%s>\n' "${a[@]}"             # <x> <y> <z w> — ALWAYS this form
echo "${#a[@]} ${!a[@]}"              # 3, indices `0 1 2`
echo "${a[@]:1:2} ${a[@]: -2}"        # slices (space before negative, like ${v: -2})
unset 'a[1]'; declare -p a            # ([0]=x [2]="z w") — HOLE
echo "${#a[@]} [${a[1]-unset}]"       # 2 [unset]
a[10]=ten; echo "${!a[@]} ${#a[@]}"   # 0 2 10, 3 — sparse allowed
```
`"${a[*]}"` joins with first char of `IFS` into ONE word (`f "${a[*]}"` = single arg). `IFS=:` demo: `"[${a[*]}]"` → `[x:y:z w]`.

## Assoc (bash 4+; NOT on macOS bash 3.2)
```bash
declare -A m; m=([k1]=v1 [k2]="v 2"); m[k3]=v3
k=k1; echo "${m[$k]} ${m[k1]}"   # v1 v1 — subscript expands
echo "${!m[@]} ${#m[@]}"         # keys + count (order undefined!)
for k in "${!m[@]}"; do echo "$k=>${m[$k]}"; done
unset 'm[k2]'; declare -p m
echo "${m[@]/v/V} ${m[@]#v}"     # per-element pat ops work on BOTH array types
```

## Fill from text
```bash
printf 'l1\nl2\nl3\n' | { mapfile -t arr; declare -p arr; }
# arr=([0]=l1 [1]=l2 [2]=l3) — -t strips newlines; no -t keeps them
# opts: -n count, -s skip, -O origin, -d delim, -u fd
# e.g. skip header, take 2: mapfile -t -s 1 -n 2 r < file
line="a b  c"; read -ra arr <<< "$line"   # ([0]=a [1]=b [2]=c)
line="a,b,c"; IFS=, read -ra parts <<< "$line"
printf 'a\0b\0' | { mapfile -d '' -t nz; declare -p nz; }  # NUL-delimited (find -print0)
```

## Pitfalls

- `a=$list` (no parens) makes a string, not array. `a=($list)` splits+globs — usually wrong; use `read -ra` or `mapfile`.
- `for x in ${a[@]}` unquoted re-splits elements with spaces. Always `"${a[@]}"`.
- Assoc without `declare -A` silently becomes indexed (`m=([k]=v)` → index 0). Declare first.
- Holes: `${a[1]}` after unset is empty but `${#a[@]}` counts 2 — iterate `"${a[@]}"` or `"${!a[@]}"`, never `{0..n}`.

## Try it

```bash
bash -c 'a=(x y "z w"); printf "<%s>\n" "${a[@]}"; echo "${#a[@]} ${!a[@]}"'
bash -c 'unset "a[1]" 2>/dev/null; a=(x y "z w"); unset "a[1]"; declare -p a; echo "${#a[@]}"'
bash -c 'declare -A m=([a]=1 [b]=2); echo "${!m[@]} ${#m[@]}"'
bash -c 'printf "l1\nl2\n" | { mapfile -t r; declare -p r; }'
```

## Optional scratch drills (inside bash-capstone/work)

1. `pkgs.sh`: array of 5 packages (one with a space to prove quoting), print each `<%s>`, print count, slice middle two.
2. `holes.sh`: unset middle element, show `declare -p`, count, and loop that still works (`"${a[@]}"`), plus loop that breaks (`{0..2}` indexing).
3. `config.sh`: assoc `host→ip` x3, lookup by `$1` with `${m[$1]:-unknown}`, list all keys, `mapfile` a file into indexed array and print numbered.

## Related

- [[04-bash-parameters|Parameters]]
- [[07-bash-loops|Loops]]

Sources: [Bash arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html). Gate: pass the inventory lab with spaced/newline filenames and deterministic bucket order; explain why associative iteration alone cannot satisfy its ordering contract.
