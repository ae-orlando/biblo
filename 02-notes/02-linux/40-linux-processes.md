---
created: 2026-10-08
updated: 2026-10-21
---

# Processes and Services

> Outcome: separate process existence, service lifecycle and application health. Practice: `linux-processes` and `bash-jobs` in [[practice-catalog]], then [[80-linux-service-incidents]]. Broad pkill and host service changes below are reference only.

## Mental model

Everything running = process with PID. `systemd` is PID 1 on Arch. Foreground blocks; `&` backgrounds; `Ctrl-Z` suspends; `jobs/fg/bg` manage shell jobs; `systemctl` manages services; `journalctl` reads the binary journal (no `/var/log/syslog` on stock Arch).

## Core commands

| Command | What it does | Example |
|---|---|---|
| `ps aux` | snapshot | `ps aux \| head` |
| `pgrep -a` | PIDs by name, no self-match (preferred) | `pgrep -af sshd` |
| `htop / btop` | interactive (install one) | `btop` (here: btop installed, htop not) |
| `kill PID / kill %1` | signal (default TERM=15) | `kill 1234; kill %1` |
| `pkill -f pattern` | signal by name | `pkill -f "node server"` |
| `jobs; fg %1; bg %1` | list / fore / background job | `sleep 60 &; jobs; fg %1` |
| `systemctl status/is-active/is-enabled` | inspect | `systemctl status NetworkManager` |
| `systemctl enable --now` | enable+start at once | `sudo systemctl enable --now sshd` |
| `systemctl cat / help` | show unit / docs | `systemctl cat sshd` |
| `journalctl` | logs | `journalctl -u sshd -e --since today` |
| `sudo dmesg / journalctl -k` | kernel ring | `journalctl -k \| tail -20` |

Signals: `TERM` (15, default, graceful) → try first. `KILL` (`-9`, uncatchable, no cleanup) → last resort only, orphans children / corrupts state.

`htop` keys (verified 3.5.3): `F3` or `/` = search, `F4` or `\` = filter (Esc exits), `F9` or `k` = kill menu, `F5` tree, `Space` tag, `u` filter-user, `F10`/`q` quit. `btop` = dashboard (CPU/mem/disk/net graphs, mouse, themes); `htop` = lighter process manager. Keep both is fine:
```bash
sudo pacman -S htop btop
```

`systemd` extras: `.service` suffix optional (`sshd` = `sshd.service`), `daemon-reload` after editing unit files in `/etc/systemd/system/`, `systemctl --failed` to find broken, user services `systemctl --user status …`, find unit from package: `pacman -Qql <pkg> | grep '\.service'`.

`journalctl` extras: `-f` follow, `-e` jump to end (implies 1000 lines), `-p err` = err+crit+alert+emerg, `--grep=PAT` (better than piping), `-b` this boot / `-b -1` previous, `--since "1 hour ago"` / `--since today`.

## Arch note

Verified here: `systemd 262`, logs in `/var/log/journal/` (persistent). **Unprivileged `dmesg` fails** (`read kernel buffer failed: Operation not permitted`) because `CONFIG_SECURITY_DMESG_RESTRICT=y` + `kernel.dmesg_restrict=1` since 5.10.4 — use `sudo dmesg` or `journalctl -k`. No `service` command — only `systemctl`.

## Pitfalls

- `kill -9` as first reflex — use plain `kill`, escalate only if ignored.
- `enable` without `--now` = next boot, not now. `start` without `enable` = now, not next boot.
- `ps aux | grep foo` matches itself — use `pgrep -af foo` or `ps aux | grep '[f]oo'`.
- `journalctl -u sshd` empty? Wrong unit name or `--user` vs system — `systemctl cat sshd` to confirm.

## Try it

```bash
sleep 60 &
jobs; pgrep -af "sleep 60"
kill %1; jobs
systemctl is-active NetworkManager; systemctl is-enabled NetworkManager
journalctl --since "1 hour ago" -p err | tail -20
journalctl -k | tail -5
```

## Related

- [[00-linux-introduction|Linux Introduction]]
- [[60-linux-networking|Networking]]
- [[90-linux-protips|Linux Protips]]

Sources: [systemd](https://wiki.archlinux.org/title/Systemd), [journal](https://wiki.archlinux.org/title/Systemd/Journal), [proc status](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html). Check: inspect a precise owned process, explain parent/group identity and reap a stopped worker. TERM requests termination; it does not guarantee graceful shutdown. A running/enabled service does not establish HTTP health.
