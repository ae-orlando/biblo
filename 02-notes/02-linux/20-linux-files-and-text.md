---
created: 2026-10-08
updated: 2026-10-21
---

# Files and Text (Pipes Wizardry)

> Outcome: preserve record boundaries and interpret pipeline status. Practice: `bash-quoting` and `bash-pipeline` in [[practice-catalog]]. Use fixture files, not a recursive search of private home-directory content.

## Mental model

Every process has stdin (0), stdout (1), stderr (2). `|` chains stdout→stdin. `>` overwrite, `>>` append, `2>` stderr, `2>/dev/null` hide errors, `2>&1` merge stderr into stdout, `|&` = `2>&1 |`. `tee` splits to file + screen. `<<EOF` feeds a heredoc.

## Core commands

| Command | What it does | Example |
|---|---|---|
| `touch / mkdir -p` | create file / nested dirs | `mkdir -p a/b && touch a/b/n.md` |
| `cp -r / mv / rm -i` | copy-tree / move / prompt-delete | `cp -r a b; mv b c` |
| `cat / less` | dump / paged (`q` quit, `/` search) | `less /var/log/pacman.log` |
| `head -n / tail -n / tail -f` | first / last / follow | `tail -n 20 -f /var/log/pacman.log` |
| `>` / `>>` / `2>` | overwrite / append / stderr | `echo hi > f; echo err 2> e.log` |
| `tee` | write file + passthrough | `echo hi \| tee f \| wc -c` |
| `grep / rg -n` | search (prefer `rg`) | `rg -n "multilib" /etc/pacman.conf` |
| `sort / uniq -c / wc -l` | sort / count-dupes / count | `sort f \| uniq -c \| sort -nr` |
| `cut -d / awk` | columns | `echo a:b | cut -d: -f2` |
| `sed 's/a/b/g'` | stream replace | `sed 's/foo/bar/g' f` |
| `diff -u` | unified compare | `diff -u a.txt b.txt` |
| `xargs -0` | NUL-framed arguments | use find -print0 or fd -0 with xargs -0; add the tool's option terminator |

Wizard pipeline (top errors):
```bash
rg -n "ERROR" app.log | cut -d: -f1 | sort | uniq -c | sort -nr | head
```

Heredoc (write multi-line without editor):
```bash
mkdir -p .practice-runtime/scratch
cat > .practice-runtime/scratch/demo.txt <<'EOF'
line1 $NOT_EXPANDED
line2
EOF
```

## Arch note

```bash
sudo pacman -S ripgrep fzf
```
`rg` respects `.gitignore`, skips hidden + binary by default. Include dotfiles: `rg --hidden pattern`. Truly everything: `rg -uu pattern` (= `--no-ignore --hidden`). Prefer `journalctl --grep=PATTERN` over `journalctl | grep` (preserves pager). `/var/log/pacman.log` is plain text — `tail -f` works. System journal is binary — use `journalctl`, not `cat`.

## Pitfalls

- `>` silently clobbers — `set -o noclobber` makes `>` fail if exists (override with `>|`).
- `grep -r` without `-n` loses line numbers; binary garbles terminal — `rg -n` handles both.
- `sort | uniq` without first `sort` undercounts (uniq only dedupes adjacent).
- `sed -i` edits in place with no undo — test without `-i` first.

## Try it

```bash
echo -e "b\na\nb\nc" | sort | uniq -c | sort -nr
rg -n "Phase" ~/Documents/Notes/01-roadmap/master-plan.md
rg -n "Outcome" 02-notes/02-linux --glob '*.md' | head -5
tail -n 20 /var/log/pacman.log
printf 'hello\n' | tee .practice-runtime/scratch/t.txt | wc -c
```

## Related

- [[10-linux-filesystem-navigation|Filesystem Navigation]]
- [[70-linux-shell-workflow|Shell Workflow]]
- [[40-linux-processes|Processes]]

Sources: [Bash redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html), [GNU find/xargs](https://www.gnu.org/software/findutils/manual/). Check: detect a late invalid record without partial success output; explain how pipefail and explicit status inspection differ from assuming the last command proves the whole pipeline worked.
