---
created: 2026-10-08
updated: 2026-10-21
---

# Arch Packages (pacman + AUR)

> Outcome: distinguish repository metadata, installed state, package ownership and untrusted build recipes. Follow [[linux-learning-path]]; package install/remove, mirror, AUR and service commands here are VM-only or separately authorized host administration. No host package changes are part of the rebuild.

## Mental model

`pacman` owns `/usr` from official repos (`core`, `extra`, `multilib` disabled by default). AUR = user PKGBUILD recipes built locally via `makepkg` / `yay` / `paru`. Rolling release assumes full upgrades — partial upgrades break.

Golden rule: **never `pacman -Sy <pkg>`**. Always `pacman -Syu`. `-Syyu` only when mirrors are broken/out-of-sync.

## Core commands

| Command | What it does | Example |
|---|---|---|
| `sudo pacman -Syu` | full upgrade (the only upgrade) | `sudo pacman -Syu` |
| `sudo pacman -S` | install | `sudo pacman -S ripgrep fzf tree` |
| `sudo pacman -Rns` | remove + unneeded deps + no backup | `sudo pacman -Rns oldpkg` |
| `pacman -Ss / -Si` | search remote / info remote | `pacman -Ss firefox` |
| `pacman -Qs / -Qi` | search installed / info installed | `pacman -Qs linux` |
| `pacman -Qdtq` | inspect orphan candidates | review each candidate and reverse dependencies before any deliberate removal |
| `pacman -Ql / -Qo / -Fl` | files owned / owner of file / remote files | `pacman -Qo /etc/pacman.conf` |
| `checkupdates` | safe pending list (no `Sy` risk) | `checkupdates \| head` |
| `paccache -r` | clean cache, keep last 3 | `paccache -d` (dry-run first) |

An orphan-candidate list is not a deletion approval. Review names, installed reasons and intended usage before removal. Danger flags include -Rsc (dependents), -Rdd (skips checks) and -Scc (empties useful rollback cache). Cache retention and automation need a separate policy.

## Arch note (verified pacman 7.1.0)

`paccache` + `pacdiff` + `checkupdates` all come from one package:
```bash
sudo pacman -S pacman-contrib
pacman -Qo /usr/bin/paccache  # pacman-contrib 1.13.1
```

`.pacnew` = your modified config + upstream shipped different version. Find and merge, never blindly overwrite:
```bash
find /etc -name '*.pacnew' -o -name '*.pacsave'
DIFFPROG=nvim\ -d pacdiff -s   # -s = sudo, -o = list only
```

Enable `multilib` (Steam/Wine) — uncomment exactly these in `/etc/pacman.conf`, then `-Syu`:
```
[multilib]
Include = /etc/pacman.d/mirrorlist
```

Mirrors — country filter discouraged (distance ≠ throughput), prefer global HTTPS + rate sort. Backup first:
```bash
sudo cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak
sudo pacman -S reflector
sudo reflector --protocol https --latest 20 --age 12 --sort rate --save /etc/pacman.d/mirrorlist
```
Automate via `/etc/xdg/reflector/reflector.conf` + `reflector.timer`.

Before big `Syu` after weeks offline: read https://archlinux.org/news/ (manual interventions posted there).

## AUR (yay/paru are AUR-only, never sudo the build)
```bash
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si
```
Same for `paru`. Flow for any AUR pkg: `git clone <url>` → `less PKGBUILD` → `makepkg -si` as **normal user**. Helpers run as user; only the `-i` step escalates.

## Pitfalls

- `pacman -Sy foo` today, broken system tomorrow — full `-Syu` or nothing.
- `yay` with sudo — breaks ownership, runs untrusted build as root.
- Ignoring `.pacnew` for months — config drift, merge with `pacdiff`.
- `pacman -Scc` to "save space" — use `paccache -r` instead.

## Try it

```bash
pacman -Qs | wc -l
pacman -Qdt
checkupdates | head -20
grep -n "multilib" -A1 /etc/pacman.conf
tail -n 10 /var/log/pacman.log
```

## Related

- [[30-linux-permissions|Permissions]]
- [[40-linux-processes|Processes]]
- [[90-linux-protips|Linux Protips]]

Sources: [pacman](https://wiki.archlinux.org/title/Pacman), [maintenance](https://wiki.archlinux.org/title/System_maintenance), [AUR](https://wiki.archlinux.org/title/Arch_User_Repository). Practice: inspect installed/owner metadata read-only, explain a partial-upgrade risk, and design a VM-tested recovery plan. Package versions and repository availability must be rechecked; historical “verified” labels are not current host facts.
