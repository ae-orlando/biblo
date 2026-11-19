---
created: 2026-10-08
updated: 2026-10-21
---

# Permissions and Ownership

> Outcome: diagnose a path's effective access and make narrow changes only in a marked sandbox. Practice: `linux-permissions` in [[practice-catalog]]. sudo/chown/sudoers examples are administration reference, never automatic course setup.

## Mental model

Files have an owner, group and mode bits; ACLs, mount options and security policy can add other access constraints. Directory x permits search/traversal; r permits listing names. Inspect the actual identity/groups instead of assuming a UID/group from an old note. umask clears bits from requested creation modes: typically `0777 & ~umask` for directories and `0666 & ~umask` for regular files. It is not general arithmetic subtraction: umask 027 ordinarily gives directories 750 and files 640.

Numeric: `7=rwx 6=rw- 5=r-x 4=r-- 0=---`. Common: files `644`, dirs `755`, scripts `755`, SSH keys `600`.

## Core commands

| Command | What it does | Example |
|---|---|---|
| `ls -l` | mode + owner | `ls -l /etc/pacman.conf` |
| `stat -c '%a %U:%G %n'` | machine-readable mode | `stat -c '%a %U:%G %n' ~/.ssh/id_*` |
| `chmod 644 / +x / -R` | set mode | `chmod +x run.sh; chmod 644 notes.md` |
| `chown user:group / -R` | change owner | `sudo chown orlando:orlando file` |
| `umask` | default mask | `umask 022` |
| `id; groups` | who + memberships | `id; groups` (`wheel` = sudo) |
| `namei -l` | per-component path perms | `namei -l ~/Documents/Notes` |
| `sudo / sudo -i / sudoedit` | run / root shell / safe edit | `sudoedit /etc/pacman.conf` |

`sudoedit` (aka `sudo -e`) copies to temp, edits as you, writes back as root — safer than `sudo nano` (editor config as root).

## Arch note

You're in `wheel` (verified). If sudo ever breaks on a fresh install: uncomment in `/etc/sudoers` via `visudo`:
```
%wheel ALL=(ALL:ALL) ALL
```
`namei` is in `util-linux` (base, always present). Pacman, `/etc`, `systemctl --system` need sudo. Never `chmod 777` to "fix" — `namei -l` the path and fix the owner.

## Pitfalls

- Broad chmod 777 destroys meaningful permission distinctions; do not “repair” it with another blanket recursion. Restore known modes from a trusted baseline and diagnose affected services/data. Ownership is a different property and may not need changing.
- A permission-denied execution can involve file execute bits, parent traversal, a noexec mount, interpreter access or security policy. Omitting ./ when a command is not on PATH ordinarily causes command-not-found, a different observation.
- `/etc` edit fails in editor = forgot sudo — use `sudoedit`, check `:w!` errors mean the same thing.

## Try it

```bash
touch demo.sh && echo 'echo hi' > demo.sh
./demo.sh || true
chmod +x demo.sh && ./demo.sh
stat -c '%a %U:%G %n' demo.sh
rm demo.sh
namei -l ~/Documents/Notes
id; umask
```

## Related

- [[00-linux-introduction|Linux Introduction]]
- [[50-arch-packages|Arch Packages]]
- [[90-linux-protips|Linux Protips]]

Sources: [Arch permissions](https://wiki.archlinux.org/title/File_permissions_and_attributes), [umask](https://man7.org/linux/man-pages/man2/umask.2.html). Check: pass the marked-sandbox lab, explain each mode and why read-only file permission does not alone control deletion from a writable parent directory.
