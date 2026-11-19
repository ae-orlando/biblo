---
created: 2026-10-08
updated: 2026-10-21
---

# Networking (ip, ssh, curl)

> Outcome: distinguish DNS/routing/transport/TLS/HTTP observations. Practice: `linux-network` in [[practice-catalog]]. SSH, resolver and host-network changes below are administration reference; do not change them merely to follow the course.

## Mental model

Interface has IP, DNS resolves names, ports pick the app. `ip` (from `iproute2`, in `base`) replaced `ifconfig`; `ss` replaced `netstat` (`net-tools` deprecated 2011, only install for old tutorials). `ssh` = encrypted remote shell, `curl` = speak HTTP, `nmcli` = control NetworkManager.

## Core commands

| Command | What it does | Example |
|---|---|---|
| `ip -brief a` | interfaces + IPs (compact) | `ip -brief a; ip r` |
| `ping -c 3` | reachability | `ping -c 3 archlinux.org` |
| `ss -tulpn` | listening TCP+UDP, numeric | `sudo ss -tulpn` (sudo = all procs) |
| `curl -I / -LO` | headers / download+follow | `curl -I https://archlinux.org` |
| `sftp / rsync -avz` | modern file copy (prefer over scp) | `rsync -avz notes.md user@host:~/` |
| `ssh` | remote shell | `ssh user@host` |
| `ssh-keygen + ssh-copy-id` | key auth | `ssh-copy-id user@host` |
| `nmcli` | NetworkManager CLI | `nmcli device status` |

`t,u,l,p,n` = TCP, UDP, listening, processes, numeric (no DNS resolve = fast). Without sudo, `-p` shows only your processes, others as `-` — use `sudo ss -tulpn` for full view (verified: own `spotify` PIDs visible unprivileged, system ones need sudo).

`curl` combos: `-I` HEAD only, `-O` save remote name, `-L` follow redirects, `-LO` together. `wget` (`extra/wget`, not base) adds `-c` resume: `wget -c <url>`.

`scp` legacy: since OpenSSH 9 `scp` runs over SFTP anyway; `-O` forces old protocol. Prefer `sftp user@host` (interactive) or `rsync -avz` (resume, deltas).

## Arch note (verified: NM active, resolved inactive here)

```bash
sudo pacman -S networkmanager openssh
sudo systemctl enable --now NetworkManager
sudo systemctl enable --now sshd   # unit is sshd.service, disabled by default
sudo sshd -t                       # test config before restart
```
Check: `systemctl is-active sshd`, `ss -tln 'sport = :22'`. `systemd-resolved` is **optional** — this machine has it `inactive`, so `resolvectl status` fails with `Unit dbus-org.freedesktop.resolve1.service not found`. That's expected if NM writes `/etc/resolv.conf` directly. To use resolved: `systemctl enable --now systemd-resolved` + symlink `/etc/resolv.conf -> ../run/systemd/resolve/stub-resolv.conf`. Firewall off by default — add `ufw`/`firewalld` if exposed to LAN/internet.

## Pitfalls

- An SSH hang can involve DNS, routing, transport filtering, server load or protocol/authentication behavior. Inspect a bounded verbose connection and relevant listener/log evidence. Ping failure does not prove TCP is blocked, and ping success does not prove SSH/HTTP works.
- `ifconfig`/`netstat` paste from old blog — use `ip a` / `ss -tulpn`, or `sudo pacman -S net-tools` as crutch.
- Bare `curl <url>` of ISO dumps binary to terminal — use `-O` or `| less`.

## Try it

```bash
ip -brief a; ip r
ss -tulpn | head -20
sudo ss -tulpn | head -20
curl -I https://archlinux.org
nmcli device status; nmcli connection show
systemctl is-active NetworkManager sshd
```

## Related

- [[40-linux-processes|Processes]]
- [[70-linux-shell-workflow|Shell Workflow]]
- [[90-linux-protips|Linux Protips]]

Sources: [Network configuration](https://wiki.archlinux.org/title/Network_configuration), [OpenSSH](https://wiki.archlinux.org/title/OpenSSH), [curl manual](https://curl.se/docs/manpage.html). Check: classify local 200/404/503/302 responses separately from connection failure; explain why a redirect must not silently bypass the lab's loopback-only policy.
