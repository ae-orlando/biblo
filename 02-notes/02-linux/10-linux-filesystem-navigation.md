---
created: 2026-10-08
updated: 2026-10-21
---

# Filesystem Navigation

> Outcome: distinguish absolute/relative paths, links and mounted filesystems while preserving filename boundaries. Practice: `bash-quoting` and `linux-permissions` in [[practice-catalog]]. Install examples below are administration reference, not prerequisites.

## Mental model

Single tree at `/`. No drive letters. `~` = `/home/orlando`, `.` = here, `..` = up, `-` = previous dir (`cd -`). Paths absolute (`/etc/pacman.conf`) or relative (`../notes`). `pushd/popd` are bash/zsh builtins, not separate binaries.

## Core commands

| Command | What it does | Example |
|---|---|---|
| `pwd` | where am I | `pwd` |
| `ls -lah` | long + hidden + human | `ls -laht` (t = newest first) |
| `cd` | move (`-` = back) | `cd ~/Documents/Notes; cd -` |
| `stat` | full metadata | `stat /etc/pacman.conf` |
| `pushd / popd / dirs -v` | dir stack | `pushd /etc; dirs -v; popd` |
| `tree -L 2 --dirsfirst` | nested view | `tree -L 2 --dirsfirst ~/Documents` |
| `find` | precise search | `find ~ -name "*.md" -not -path "*/.*"` |
| `fd` | fast `find` | `fd '\.md$' ~/Documents` |
| `realpath` | resolve full path | `realpath ./notes.md` |

`fd` defaults (binary `fd`, package `fd`): regex, respects `.gitignore`, skips hidden. Include hidden: `fd -H pattern`. Include ignored too: `fd -I` / both `fd -u`. So `find ~ -name "*.md" -not -path "*/.*"` ≈ `fd '\.md$' ~` (without dotfiles) vs `fd -H '\.md$' ~` (with).

`ls` flags: `-l` long, `-a` all, `-h` human, `-t` time-sort, `-R` recursive, `-1` one per line (for pipes).

## Arch note

```bash
sudo pacman -S tree fd
```
`iproute2` (provides `ip`) is in `base`; legacy `net-tools` (`ifconfig`) deprecated since 2011 — only install if following an old tutorial: `sudo pacman -S net-tools`.

## Pitfalls

- Spaces: `cd "My Notes"`, never bare `cd My Notes`.
- An empty DIR in a destructive glob can select the wrong tree. Adding -- or nounset does not reject an explicitly empty value. Do not run broad delete examples as practice: validate a nonempty expected owned scratch path and its resolved boundary first, and prefer removing only known files or an empty unique directory. Preview output alone is not a safety proof.
- Bare `ls` hides `.*` — use `-a`. `tree` on `/` floods — always `-L 2`.

## Try it

```bash
pwd; ls -laht | head
cd ~/Documents/Notes && tree -L 2 --dirsfirst
fd '\.md$' . | head -20
fd -H '\.md$' . | wc -l
pushd /etc && dirs -v && popd
stat /etc/pacman.conf
```

## Related

- [[00-linux-introduction|Linux Introduction]]
- [[20-linux-files-and-text|Files and Text]]
- [[90-linux-protips|Linux Protips]]

Sources: [Core utilities](https://wiki.archlinux.org/title/Core_utilities), [GNU find](https://www.gnu.org/software/findutils/manual/), [GNU coreutils](https://www.gnu.org/software/coreutils/manual/). Check: pass the arbitrary-filename lab, then explain a symlink versus its target and why a path prefix alone is not a resolved containment check.
