---
created: 2026-10-08
updated: 2026-10-21
---

# 03 — Quoting, Splitting, Globbing

> Prerequisite: [[02-bash-expansions]]. Outcome: preserve data as arguments while intentionally choosing pattern semantics. Practice: `bash-quoting` in [[practice-catalog]].

## Mental model

After expansions, bash splits unquoted results on `IFS` (default space/tab/newline), then glob-matches `* ? [` against files. Quotes suppress both. `[[ ]]` and `case` words skip splitting/globbing — safe unquoted there. Rule: **quote by default, unquote deliberately.**

```bash
var='a  b   c'
printf '<%s>\n' $var    # <a> <b> <c> — split into 3
printf '<%s>\n' "$var"  # <a  b   c> — one field
```

## Quoting forms

| Form | Expands | Use |
|---|---|---|
| `'...'` | nothing (can't embed `'`) | literals: `'*.txt'`, `'a b'` |
| `"..."` | parameter, command and arithmetic expansion; selected backslashes | default arguments: `"$file"` |
| `\x` | next char literally | spaces: `My\ Notes`, `\$` |
| `$'...'` | ANSI-C `\n \t \\ \' \" \xHH \uHHHH` | `echo $'a\nb'` |
| `$"..."` | locale gettext (else same as `"`) | i18n scripts |
| `$( )` | new quoting context inside | `"a $(b "$c")"` — quote at both levels |

`\` inside `"..."` stays literal except before `$ ` " \ newline`. Line continuation: `\<newline>` joins lines.

## Splitting (`IFS`)
Only results of parameter/command/arithmetic expansion, when **unquoted**, are split. Unexpanded words never split.
```bash
printf 'a:b::c\n' | { IFS=: read -r a b c d; echo "<$a> <$b> <$c> <$d>"; }
# <a> <b> <> <c> — non-whitespace IFS: adjacent delims = empty field
printf '  a  b \\\n' | { IFS= read -r line; echo "<$line>"; }
# IFS= preserves whitespace, -r preserves backslashes — THE file-reading idiom
```
SC2086 (`echo $1`), SC2046 (`ls -l $(getf)` → `"$(getf)"`), intentional split → use array instead: `opts=(-j 5); make "${opts[@]}"`.

## Globbing (after splitting, unquoted `* ? [` only)
```bash
echo *.txt [ab].txt ?.txt     # match files
echo "*.txt"                  # literal — quoting suppresses
echo nomatch_*                # literal when nullglob off (default)
shopt -s nullglob   # non-match expands to NOTHING (for loops)
shopt -s failglob   # non-match is an ERROR (safe rm patterns)
shopt -s dotglob    # * includes dotfiles (. and .. still excluded)
shopt -s globstar   # ** = all dirs recursively: **/*.md
shopt -s nocaseglob # case-insensitive paths
set -f              # set -o noglob: disable globbing (not splitting)
```
Keep globs outside quotes: `"$dir"/*.c` (right) vs `"$dir/*.c"` (literal, wrong). `rm *` vs file named `-f` → `rm ./*` or `rm -- *` (SC2035).
A nonempty GLOBIGNORE removes matching names and also enables dotglob-like inclusion of other hidden names; `.` and `..` remain special. Unsetting it disables that side effect. Account for the previous shell state rather than using it as a side-effect-free filter.

## Extended glob `extglob` (pattern language for `[[ == ]]`, `case`, `${v//pat/}`)
```bash
shopt -s extglob
f=foo123.txt
[[ $f == +(a|f)*.txt ]] && echo plus    # +(pat): ONE or more
[[ $f == @(foo|bar)* ]] && echo at      # @(pat): EXACTLY one
[[ $f == !(bar)* ]] && echo not-bar     # !(pat): anything EXCEPT
[[ $f == ?(f)oo* ]] && echo maybe       # ?(pat): ZERO or one
[[ $f == *([0-9]).txt ]] && echo stars  # *(pat): ZERO or more
# Same in case arms and parameter replace: echo "${f//+([0-9])/N}"
```
`[[ == ]]` treats unquoted RHS as pattern *as if extglob were on* even when `shopt` is off — but filename globs on disk still need `shopt -s extglob`. Prefer enabling it explicitly.

`[[ == ]]` RHS is a pattern: `[[ f.txt == *.txt ]]` matches; `[[ f.txt == "$v" ]]` with `v='*.txt'` does NOT (quoted = literal). `case` arms are globs too.

## Pitfalls

- `for f in $(ls)` — splits on spaces AND globs. Use `for f in *` or `while read`.
- nullglob changes unmatched pathname expansion, not the -e test inside [[ ]], where pathname expansion does not occur. It can remove an unmatched unquoted argument before an external command sees it. Restore the prior setting or confine changes to a subshell when appropriate.
- `echo $var` with `var='*'` lists your directory. Quote.
- `!(pat)` in interactive shell collides with history expansion — test extglob in scripts/`bash -c`, or `set +H`.
- macOS bash 3.2: no `**` even with `shopt -s globstar`. Use `find`.

## Try it

```bash
bash -c 'v="a  b *"; printf "<%s>\n" $v; printf "<%s>\n" "$v"'
mkdir -p .practice-runtime/scratch/globs
bash -c 'cd .practice-runtime/scratch/globs && touch a.txt b.txt && printf "<%s>\n" *.txt "*.txt"'
bash -c 'shopt -s nullglob; echo START; echo nomatch_xyz_*; echo END; shopt -u nullglob'
bash -c '[[ abc.txt == *.txt ]] && echo pat; v="*.txt"; [[ abc.txt == $v ]] && echo unquoted-var-pat'
bash -c 'shopt -s extglob; f=foo123.txt; [[ $f == +(a|f)*.txt ]] && echo plus; [[ $f == !(bar)* ]] && echo not-bar'
```

## Optional scratch drills (inside bash-quoting/work)

1. `split.sh`: `v='a  b *'` — print with/without quotes via `printf '<%s>\n'`; comment the word counts.
2. `glob.sh`: in a scratch dir with `a.txt b.txt -f`, show `echo *`, `echo "*.txt"`, `rm -- *` safety, `shopt -s nullglob` loop over empty match.
3. `pattern.sh`: compare unquoted pattern versus quoted literal RHS in [[ ]], and a case arm `[Bb]ar*`. For extglob digits, use `+([0-9])` versus `*([0-9])`; `+(0-9)` repeats the literal text `0-9`, not a digit range.

## Related

- [[02-bash-expansions|Expansions]]
- [[04-bash-parameters|Parameters]]
- [[14-set-shopt-strict-debug|Set/Shopt/Strict Mode]] (`shopt` catalog)

Sources: [Bash quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html), [filename expansion](https://www.gnu.org/software/bash/manual/html_node/Filename-Expansion.html), [ShellCheck SC2086](https://www.shellcheck.net/wiki/SC2086). Gate: pass the filename lab and explain why a newline separator cannot represent arbitrary filenames.
