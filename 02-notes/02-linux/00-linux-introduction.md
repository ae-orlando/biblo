---
created: 2026-10-08
updated: 2026-10-21
---

# Linux Introduction (Arch)

> Outcome: distinguish kernel, userland, shell and program, and find authoritative help. Follow [[linux-learning-path]] for assessed practice. Package installation and host administration snippets are optional VM/reference material, not commands the rebuild executes.

## Mental model

Linux names the kernel; a distribution combines it with userland and package/configuration policies. “Everything is a file” is a useful interface metaphor, not a literal statement about every kernel object. /dev exposes device nodes, /proc virtual process/kernel information and /etc system configuration.

Layout: `/` root, `/home` your files, `/etc` system config, `/usr/bin` programs (pacman owns `/usr`), `/var/log/pacman.log` + `/var/cache/pacman/pkg`, `/boot` kernel/initramfs, `/tmp` throwaway (tmpfs).

Help order: `--help` → `man` → `tldr` → Arch Wiki → random blogs last.

## Core commands

| Command | What it does | Example |
|---|---|---|
| `uname -a` | kernel + arch | `uname -a` |
| `man <cmd>` | full manual | `man pacman` |
| `man -k <word>` | search man pages | `man -k partition` |
| `<cmd> --help` | quick usage | `ls --help` |
| `tldr <cmd>` | practical examples | `tldr tar` |
| `command -v <cmd>` | where it resolves (preferred) | `command -v python3` |
| `type <cmd>` | builtin/alias/file? | `type cd` |
| `lsblk -f` | disks + fstype + mountpoints | `lsblk -f` |
| `fastfetch` | system summary | `fastfetch` |

`command -v` beats `which`: `which` is external `/usr/bin/which` and misses builtins (`which cd` fails, `type cd` works).

## Arch note

Install docs tools once (two `tldr` clients conflict — pick one):
```bash
sudo pacman -S man-db tealdeer fastfetch
tldr --update
```
`neofetch` is dead upstream (archived Apr 2024) and gone from Arch repos — use `fastfetch`. Rolling = `sudo pacman -Syu` often, and read https://archlinux.org/news/ before big upgrades after weeks offline. Safe pending check: `checkupdates` (from `pacman-contrib`, no partial-upgrade risk).

Use current observations instead of an old assumed installation biography. SHELL normally reports the configured login shell, not necessarily the interpreter running the current command. Run Bash examples explicitly with Bash. Existing dotfiles are outside this rebuild and are not inspected/changed to “fix” historical claims.

## Pitfalls

- Ubuntu paste with `apt-get` / `ifconfig` / `service` — translate to `pacman` / `ip` / `systemctl`.
- `arch-news` command doesn't exist — it's the website + `checkupdates` / `informant` (AUR).
- Running as root full-time — use normal user (`orlando:wheel`) + `sudo`.

## Try it

```bash
uname -a
command -v bash; type cd
man man; man -k mirror
lsblk -f
fastfetch
checkupdates | head
```

## Related

- [[10-linux-filesystem-navigation|Filesystem Navigation]]
- [[50-arch-packages|Arch Packages]]
- [[90-linux-protips|Linux Protips]]

Sources: [Arch system maintenance](https://wiki.archlinux.org/title/System_maintenance), [Arch installation guide](https://wiki.archlinux.org/title/Installation_guide). Check: identify a builtin versus an external program, explain the current directory and demonstrate use of a manual. Continue into the actual labs in [[practice-catalog]].
