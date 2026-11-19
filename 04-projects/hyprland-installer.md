---
created: 2026-10-08
updated: 2026-10-08
---

# Hyprland Installer (project spec)

> **Rebuild boundary, 2026-10-21:** retain this external-project specification; do not run its package, AUR, Stow, portal, display-manager or dotfile commands as vault setup. Version/API/package claims below are historical and need current upstream/local verification before implementation. Current learning prerequisites are [[00-how-to-use-track]], [[linux-learning-path]] and [[30-script-workflow]]. Bundled training code lives inside the vault; existing ~/dotfiles/ and other external code remain untouched.

Goal: one command rebuilds your Hyprland desktop on a fresh Arch install: `~/dotfiles/install.sh --dry-run` → review → `~/dotfiles/install.sh --yes`. Tested in VM snapshot first, never blind on hardware.

Status: spec — implement in `~/learning/arch-setup/` or `~/dotfiles/`, not in notes. Notes hold the design; code lives outside Obsidian per roadmap rules.

## Verified baseline (this machine)
- `hyprland 0.56.2` installed, config is Lua: `/usr/share/hypr/hyprland.lua` (default) + `~/.config/hypr/hyprland.lua` (yours). **≥0.55 uses Lua — do NOT write `hyprland.conf`/`exec-once` for new installs.**
- `waybar` installed. `sddm`, `stow`, `shellcheck`, `shfmt` available in `extra`, not installed — script installs them.

## Stack (all `extra`, verified)

```bash
OFFICIAL=(
  hyprland
  xdg-desktop-portal-hyprland xdg-desktop-portal-gtk
  waybar kitty foot wofi rofi
  sddm hyprpolkitagent polkit
  wl-clipboard cliphist grim slurp swappy
  hyprpaper hypridle hyprlock
  mako                        # or swaync — pick one, some apps freeze with none
  brightnessctl playerctl pamixer pavucontrol
  pipewire wireplumber pipewire-pulse pipewire-alsa
  bluez bluez-utils blueman network-manager-applet
  qt5-wayland qt6-wayland
  ttf-jetbrains-mono-nerd     # + a sans-serif or squares
  mesa                          # AMD/Intel; NVIDIA: read Hyprland Nvidia page first
  stow reflector shellcheck shfmt git base-devel
)
```

Notes: `rofi` now provides `rofi-wayland` (merged). Wallpaper: prefer native `hyprpaper` (`swww` renamed to `awww`). Portal needs BOTH `xdg-desktop-portal-hyprland` + `-gtk` (no file picker without gtk). Upstream default terminal bind is `kitty` (`SUPER+Q`).

## Config layout (Lua, ≥0.55)

```
~/dotfiles/
  install.sh            # this spec
  packages.txt          # OFFICIAL + AUR lists (one per line, for review)
  hypr/.config/hypr/
    hyprland.lua        # main, split via require()
    hyprpaper.conf hypridle.conf hyprlock.conf
    modules/            # binds, monitors, rules
  waybar/.config/waybar/
  foot/.config/foot/
```

Autostart = Lua, not `exec-once`:
```lua
hl.on("hyprland.start", function()
  hl.exec_cmd("waybar")
  hl.exec_cmd("hyprpaper")
  hl.exec_cmd("hypridle")
  hl.exec_cmd("systemctl --user start hyprpolkitagent")
end)
```
`hl.exec_cmd()` is async (no `&`). Old `exec-once = waybar & ...` is ≤0.54 only. Launch: `start-hyprland` from TTY (no sudo), or DM: `sudo systemctl enable sddm.service` (SDDM ≥0.20 fine; GDM crashes first launch per wiki).

## install.sh phases

```bash
#!/usr/bin/env bash
set -euo pipefail
# 0. guards: (( EUID != 0 )), sudo -v, --dry-run/--yes via getopts
# 1. upgrade: sudo pacman -Syu --needed --noconfirm
# 2. official: sudo pacman -S --needed --noconfirm "${OFFICIAL[@]}"
# 3. helper: pick paru/yay or build yay (base-devel+git, makepkg -si as user)
# 4. AUR: "$HELPER" -S --needed --noconfirm --noremovemake --answerclean All --answerdiff None "${AUR[@]}"
# 5. dotfiles: [[ -d ~/dotfiles ]] || git clone <url> ~/dotfiles; cd ~/dotfiles && stow -t ~ hypr waybar foot
# 6. services: sudo systemctl enable --now sddm bluetooth; systemctl --user enable --now hyprpolkitagent
# 7. verify (below) + print .pacnew check + reboot prompt
```

Every destructive call through `run()` (dry-run aware). Every install idempotent (`-Qq` / `--needed` / `is-enabled --quiet`).

## Verify (script prints these at end)

```bash
hyprctl version
hyprctl monitors
systemctl --user status xdg-desktop-portal-hyprland --no-pager
systemctl --user status xdg-desktop-portal --no-pager
wpctl status | head -20
bluetoothctl show | head -5; systemctl is-active bluetooth
grim -g "$(slurp)" - | wl-copy && echo "screenshot->clipboard OK"
find /etc -name '*.pacnew' -o -name '*.pacsave'
```

Functional: screenshare in browser/OBS (portal picker pops), auth dialog appears (polkit), no squares (fonts), Qt apps render (qt-wayland + `dbus-update-activation-environment --systemd --all`).

## Pitfalls (from wiki, all real)
1. Missing portal package → screenshare dead. Nuclear fix: kill both portals, start `/usr/lib/xdg-desktop-portal-hyprland &`, sleep 2, `/usr/lib/xdg-desktop-portal &`.
2. Missing polkit/seat → no auth, Hyprland won't start headless. Need `hyprpolkitagent` autostart.
3. Missing fonts → squares. Missing `qt5/6-wayland` → Qt/OBS broken.
4. Writing `hyprland.conf` on 0.56 → silently ignored. Target `hyprland.lua`.
5. `NIXOS_OZONE_WL=1` is NixOS-only — ignore on Arch; Electron Wayland via `--enable-features=UseOzonePlatform --ozone-platform=wayland`.
6. NVIDIA or no-3D-accel VM → login fail/flash/black. Read Nvidia page; enable 3D in VM.
7. `--noconfirm` + no `.pacnew` review → broken configs weeks later.

## Related
- [[20-arch-automation|Arch Automation]]
- [[30-script-workflow|Script Workflow]]
- [[90-bash-protips|Bash Protips]]
- [[50-arch-packages|Arch Packages]]

Sources: ArchWiki `Hyprland`, wiki.hypr.land (`Installation`, `Must-have`, `Systemd-start`, `Autostart`), verified against local hyprland 0.56.2.
