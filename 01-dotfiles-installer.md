---
tags:
  - dotfiles
---
install.sh is a fresh-Arch reproducer: reapplies this repo onto a machine. Single file, zero deps, idempotent.
Profiles/flags: full (default, 152 official + 21 AUR) or core (111+5, bootable Hyprland only). --only-dotfiles skips system work (5 phases not 8), --no-aur skips themes/waypaper, --dry-run changes nothing, --yes non-interactive. Prompts for profile/AUR/confirm when interactive.
Phases in order:
1. phase_preflight — root/Arch gates, repo check, backup real configs to ~/.local/state/dotfiles-backup-*/home/, sudo keepalive, single-instance lock.
2. phase_base — pacman.conf Color/ParallelDownloads (+backup), reflector mirrors, pacman -Syu, bootstrap yay-bin via mktemp.
3. phase_packages — snapshot pacman -Qq, install missing official then AUR (batch → per-package retry, failures listed not fatal).
4. phase_services — write Fibocom wwan-enable.service, daemon-reload, enable 12 system + 6 user units (keeps tlp disabled).
5. phase_dotfiles — 13 symlinks (LINK_MAP), idempotent ~/.zshenv (ZDOTDIR), +x bits, runtime dirs, seed ~/Pictures/wallpapers (cp -n), seed waypaper/config.ini from example, normalize qt6ct home path, regenerate bookmarks + idempotent mimeapps.list, gsettings, fc-cache.
6. phase_shell — oh-my-zsh unattended, powerlevel10k, chsh -s zsh, zsh -n check.
7. phase_theming — one matugen image run rebuilds all 12 gitignored palette outputs.
8. phase_verify — report-only binaries/symlinks/configs/fonts/services; profile-aware (spotify on full only, waypaper unless --no-aur). Exit 1 if any FAIL (real run only).
Logs always to ~/.local/state/dotfiles-install/logs/ (last 10 kept).