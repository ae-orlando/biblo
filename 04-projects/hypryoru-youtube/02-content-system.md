---
created: 2026-10-16
updated: 2026-11-13
---

# 02 Content System

Template for every video (8-12 min):
0:00-0:30 result demo. 0:30-2:00 problem + 3 outcomes. 2:00-80% config walk + `hyprctl reload` proof. Last 20% break test + commit link. No intro logo. No goodbye — end on result + 1 spoken next-video link.

Retention: cut every 10-15s (fullscreen -> zoomed config -> reload). On-screen text for every keybind/command. Pattern interrupt at 0:30 (wipe/zoom/sound tick).

## Series (playlists)

| Series | Cadence | Covers | Source |
|--------|---------|--------|--------|
| **Build Log** | weekly, 6-10 min | any real change: dotfiles, tooling, project, system | whatever changed that week |
| **Module Guide** | bi-weekly, 10-15 min | ricing modules (evergreen search) | `~/Dev/dotfiles/<module>/` |
| **Tool Guide** | bi-weekly (alternating weeks) | YoruNeovim, tmux, zsh, terminal workflow (evergreen) | tool repo + your config |
| **Fix & Maintain** | monthly, 8-12 min | break/fix in VM + Arch maintenance (updates, backups, recovery) | VM + real maintenance work |
| **Build in Public** | monthly / as projects progress | real full-stack project logs | `~/Dev/projects/` |

Rotation: **A-A-X** until video ~20 — two ricing videos, then one rotating pillar (B → C → D → E). After video 20, rebalance by metrics (CTR + retention per pillar).

## First 12 (in order)

1. **Desk Tour 2026 — My Hyprland Setup in 3 Minutes** ✅ *shipped as the 6:34 one-take cut ([[08-video-1-script]])*
   Hook: full rice, no talking, keycast on. Goal: hook + subscribe baseline.
   Shoot: Waybar, Rofi launcher, wallpaper switch via matugen, Kitty+btop+fastfetch.

2. **HyprYoru Explained in 10 Minutes** — *shipped out of order as the zoxide Tool Guide (15:03 cut, [[09-video-2-zoxide-guide]]); slot 2 now owed as the HyprYoru deep-dive*
   Map: `README.md` structure -> `hyprland/hyprland.lua` requires -> matugen hub -> `install.sh` phases. End: repo link + commit.

3. **Fresh Arch to Hyprland With One Script (VM)**
   Run: `./install.sh --dry-run` -> `--profile core --yes` -> reboot to GDM/Hyprland. Show idempotent re-run. Warn: monitors hardcoded eDP-1, use empty-output fallback.

4. **YoruNeovim — Install My Neovim Distro** *(dev tooling — first B-pillar video)*
   Install from repo, first launch, YoruNeovim/LazyVim splash, 3 must-know binds, plugin-set tour. End: repo link.

5. **Matugen: One Wallpaper to Theme Everything** — *in production as video 3, reframed as the reliability story ([[11-video-4-dynamic-theming]]); 10–12 min, next upload*
   Run: `~/.config/hypr/scripts/set-wall.sh <wall>`. Show the coordinated pipeline regenerate 13 outputs: Waybar, Kitty, SwayNC, Rofi, btop, hyprlock, GTK/Qt, Spicetify, shell. The angle is not installation — it is validated batch publish, rollback, and recovery. Taste tip: commit to one scheme.

6. **Waybar From Scratch**
   Files: `waybar/config.jsonc` + `style` + `scripts/launch.sh`. Hard-restart demo. CPU/mem/battery widgets.

7. **My Dev Terminal Workflow** *(tooling)*
   tmux + zsh/p10k + yazi in one real task end-to-end. Show session layout, keybinds, no dead air.

8. **Building Bachiru Coffee House — Full-Stack Build Log #1** *(build in public)*
   Stack, what ships this episode, real commit. Not a tutorial — a real build with mistakes left in.

9. **Arch Maintenance: My Update + Backup Routine** *(maintenance)*
   pacman/paru cadence, snapshots, dotfiles backup, restore test. Search-heavy evergreen.

10. **I Broke My Dotfiles — Fix Live** *(break/fix)*
    Demo backup dir `~/.local/state/dotfiles-backup-*`, restore `cp -a`, re-link `--only-dotfiles`. Verify phase output.

11. **Hyprland in Lua, Not Conf**
    File: `hyprland/hyprland.lua` + `modules/general.lua`, `modules/env.lua`, `modules/monitors.lua`. Show `hyprctl reload` after each edit. Pitfall: 0.56 ignores `hyprland.conf`.

12. **Ricing Q&A + Comment Mining** *(or project log #2 if comments are thin)*
    Answer real comments; announce the next pillar.

**Backlog after 12:** Rofi type-6/style-9 + launchers · Kitty + btop + fastfetch theming · SwayNC + waypaper + GTK/Qt consistency · zsh OMZ + p10k + ZDOTDIR · second project log · VM install hardening · laptop battery/power tuning.

## Shorts (1 per long video)
Vertical crop of result demo only. No daily Shorts — unsustainable solo. 1 long = 1 Short max.
