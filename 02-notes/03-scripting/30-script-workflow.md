---
created: 2026-10-08
updated: 2026-10-21
---

# Script Workflow (edit → lint → dry-run → VM → real)

> Outcome: establish behavioral evidence and failure recovery before privileged automation. Prerequisites: Bash labs in [[practice-catalog]] and [[linux-learning-path]]. Real dotfiles/package/service changes are outside the vault rebuild and remain VM-only or separately authorized.

## Mental model

Scripts destroy fast. Workflow = small loop with gates: write 10 lines → lint → dry-run → VM snapshot → real machine. `shellcheck` finds quoting bugs, `--dry-run` previews damage, VM absorbs it. Never debug on your live Hyprland session first.

```
edit → shfmt -w → shellcheck → bash -n → --dry-run → VM → real → git commit
```

## The loop

1. **Edit small.** One function at a time. Keep package lists as arrays at top, logic in `main`.
2. **Format + lint** (install once — verified in `extra`, not installed here):
   ```bash
   sudo pacman -S shellcheck shfmt
   shfmt -i 2 -ci -bn -w install.sh
   shellcheck install.sh   # fix SC2086 (quote), SC2046, SC2181 before continuing
   bash -n install.sh      # syntax only
   ```
3. **Trace one run:**
   ```bash
bash -x install.sh --dry-run 2>&1 | sed -n '1,40p'
   PS4='+ ${BASH_SOURCE}:${LINENO}: ' bash -x install.sh --dry-run
   ```
4. **VM first.** Fresh Arch ISO in `qemu`/VirtualBox with 3D accel (Hyprland needs it; no accel = black screen, not a script bug). Snapshot → run script → `hyprctl version` → rollback on failure. Only then run on hardware.
5. **Log everything:**
   ```bash
   exec > >(tee -a setup-$(date +%F).log) 2>&1
   ```
   Keep the log next to the commit hash that produced it.
6. **Commit.** Script + package list + dotfiles commit together. Tag working states (`v1-boots`, `v2-audio`).

## When to use what

| Tool | Use when | Example |
|---|---|---|
| Alias | interactive shortcut, no args | `alias pac='sudo pacman -Syu'` |
| Function in `*rc` | interactive, needs args | `mkcd() { mkdir -p "$1" && cd "$1"; }` |
| Script in `~/.local/bin` | reused, destructive, or >10 lines | `install.sh --dry-run` |
| `systemd timer` | recurring (mirror refresh, backups) | `reflector.timer`, backup timer |
| `cron` | avoid on Arch — timers integrate with journal | `systemctl list-timers` |

## Arch note

`~/.local/bin` placement: `install -m755 install.sh ~/.local/bin/my-setup` (creates + sets 755 at once). Re-login once for PATH. Secrets (GitHub tokens, Wi-Fi PSKs): never in git — `chmod 600` file in `~/.config/secrets/` or `age`/`sops`, read via `"$(cat file)"`. GitHub push of a token = rotate immediately.

Debug checklist when installer fails:
```bash
systemctl --failed
journalctl --since "10 min ago" -p err | tail -20
find /etc -name '*.pacnew' -o -name '*.pacsave'
pacman -Qq hyprland xdg-desktop-portal-hyprland || echo MISSING
```

## Pitfalls

- `bash -x` on script with secrets leaks them to terminal/log — redact or `set +x` around that block.
- Testing Hyprland installer inside X11/nested Wayland and concluding "broken" — test on TTY or DM login, not nested.
- No snapshot before real run — one `--noconfirm` typo from reinstalling the world.

## Try it

```bash
sudo pacman -S --needed shellcheck shfmt
shellcheck --version | head -2; shfmt --version
ls ~/.local/bin/ 2>&1
systemctl list-timers --no-pager | head -10
```

## Related

- [[10-robust-bash-scripts|Robust Scripts]]
- [[20-arch-automation|Arch Automation]]
- [[90-bash-protips|Bash Protips]]

Sources: ArchWiki `systemd/Timers`, `Dotfiles`, shellcheck wiki.

## Evidence gate

Run `bash-cli` to prove dry-run and preserved output, `bash-jobs` to prove normal/TERM cleanup, and `bash-capstone` for integration. Show a test catching a deliberate bug. In a VM, record baseline state, first/second-run differences, a forced failure and a recovery attempt. An enabled service or green linter alone is not a working installer. Git commands in this reference are learner actions, not something the rebuild initializes or commits automatically.
