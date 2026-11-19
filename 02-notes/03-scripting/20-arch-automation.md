---
created: 2026-10-08
updated: 2026-10-21
---

# Arch Automation (pacman, AUR, stow, systemd in scripts)

> **VM-only administration reference.** None of these installation, AUR, mirror, dotfile or service commands is executed by the learning rebuild. First complete Bash/Linux labs and the incident worksheet in [[linux-learning-path]]. Target package/config behavior must be rechecked against current upstream documentation before a real installer.

## Mental model

An installer coordinates privileged and unprivileged side effects. Idempotence means repeated application converges to a defined desired state; checking one package is installed does not make a rolling upgrade, AUR build or whole installer a no-op. Review trust boundaries, preconditions, partial-failure recovery and rollback before enabling unattended changes.

Guard at top:
```bash
(( EUID != 0 )) || { echo "run as user, not root" >&2; exit 1; }
sudo -v   # cache credentials once
```

## Core patterns

Official packages (verified `pacman(8)` wording):
```bash
sudo pacman -Syu --needed --noconfirm
sudo pacman -S --needed --noconfirm hyprland waybar kitty
# --needed: skip up-to-date. --noconfirm: bypass all "Are you sure?" (man: only for scripts).
# NEVER pacman -Sy <pkg> — partial upgrade breaks libs. Always -Syu.
# Safe pending check (no DB touch): checkupdates | head  (from pacman-contrib)
```

AUR (helpers are AUR-only, unsupported — vet PKGBUILDs):
```bash
if command -v paru &>/dev/null; then HELPER=paru
elif command -v yay &>/dev/null; then HELPER=yay
else
  sudo pacman -S --needed --noconfirm base-devel git
  git clone https://aur.archlinux.org/yay.git /tmp/yay && (cd /tmp/yay && makepkg -si --noconfirm)
  HELPER=yay
fi
"$HELPER" -S --needed --noconfirm --noremovemake --answerclean All --answerdiff None some-aur-pkg
# Do not suppress review of untrusted PKGBUILDs merely to make a demo unattended.
# Helper flags differ by tool/version. Review build inputs and dependencies first.
```

Idempotency (verified exit codes: `pacman -Qq` 0 found / 1 missing; `is-enabled --quiet` 0 yes):
```bash
pacman -Qq hyprland &>/dev/null || sudo pacman -S --needed --noconfirm hyprland
command -v stow &>/dev/null || sudo pacman -S --needed --noconfirm stow
systemctl is-enabled --quiet sddm || sudo systemctl enable sddm
systemctl --user is-enabled --quiet hyprpolkitagent || systemctl --user enable hyprpolkitagent
[[ -L ~/.config/hypr ]] || ln -s ~/dotfiles/hypr/.config/hypr ~/.config/hypr
[[ -d ~/dotfiles ]] || git clone <url> ~/dotfiles
```

Mirrors in scripts (backup, skip if fresh):
```bash
if [[ ! -f /etc/pacman.d/mirrorlist ]] || [[ $(find /etc/pacman.d/mirrorlist -mtime +7 -print) ]]; then
  sudo cp -a /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak
  sudo reflector --protocol https --latest 20 --age 12 --sort rate --save /etc/pacman.d/mirrorlist
  sudo pacman -Syu
fi
# Better long-term: /etc/xdg/reflector/reflector.conf + systemctl enable --now reflector.timer
```

Post-upgrade check (`.pacnew` breaks software if ignored):
```bash
find /etc -name '*.pacnew' -o -name '*.pacsave'
DIFFPROG=nvim\ -d pacdiff -s
```

## Dotfiles with Stow (verified `extra/stow 2.4.1`)
```bash
sudo pacman -S --needed --noconfirm stow
# repo mirrors $HOME: dotfiles/hypr/.config/hypr/hyprland.lua -> ~/.config/hypr/hyprland.lua
cd ~/dotfiles && stow -t ~ hypr nvim tmux
stow -n -v -t ~ hypr   # dry-run
stow -R -t ~ hypr      # restow after update
stow -D -t ~ hypr      # unstow
# conflict (target exists, not a stow link): aborts safely, no deletion.
# adopt live files INTO repo: stow --adopt -t ~ hypr && cd ~/dotfiles && git diff && git commit
```
Alternatives: bare git (`git init --bare ~/.dotfiles`, no symlinks, confusing nested repos) vs `cp -r` (simple, diverges, silent overwrites). Stow wins for Hyprland (many files under `~/.config/`).

## Services in scripts
```bash
sudo systemctl enable --now sddm bluetooth   # system: needs root; --now = boot + now
sudo systemctl daemon-reload                 # after copying unit to /etc/systemd/system/
systemctl --user enable --now hyprpolkitagent  # user: NO sudo
systemctl --failed                            # verify nothing broken
```

## Arch note (verified here)

`paccache`/`pacdiff`/`checkupdates` need `sudo pacman -S pacman-contrib`. Keyring exception (NOT partial): `sudo pacman -Sy --needed archlinux-keyring && sudo pacman -Su`. Place finished script: `install -m755 install.sh ~/.local/bin/my-setup` (`~/.local/bin` already in PATH after relogin).

## Pitfalls

- Whole script under `sudo ./install.sh` — breaks yay, stow paths, `--user` units. Run as user, `sudo -v` inside.
- `--noconfirm` without post `.pacnew` check — silent config drift.
- `reflector --save` every run rewrites mirrorlist — guard by mtime or use timer.
- `yay` with default answers hangs on diff menu in CI — always pass `--answerclean/--answerdiff`.

## Try it

```bash
pacman -Qq hyprland && echo installed
command -v yay paru stow reflector
systemctl is-enabled sddm; echo "exit:$?"
checkupdates 2>&1 | head -3
```

## Related

- [[10-robust-bash-scripts|Robust Scripts]]
- [[30-script-workflow|Script Workflow]]
- [[00-linux-introduction|Linux Introduction]]

Sources: [Arch maintenance](https://wiki.archlinux.org/title/System_maintenance), [AUR helpers](https://wiki.archlinux.org/title/AUR_helpers), [Stow manual](https://www.gnu.org/software/stow/manual/), [systemd user services](https://wiki.archlinux.org/title/Systemd/User). Practice: use fixture-backed planning and a VM snapshot; explain what repeats safely and what cannot be automatically rolled back. No host deployment is claimed verified.
