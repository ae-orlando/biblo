---
created: 2026-10-19
updated: 2026-10-20
---

# 08 Video 1 — Desk Tour 2026

3-min screen-only tour, voiceover recorded after. Banked unreleased ([[06-90-day-plan]]). Goal: hook + subscribe baseline ([[02-content-system]]).

> **Final cut (2026-10-20):** 6:34 — one continuous take + a single hard cut at 4:53.5. Publishing directly (bank-3 skipped by decision). Master + thumbnail live in `~/Videos/hypryoru/export/01-desk-tour/`. Full publish package at the bottom of this note.

## Pre-flight

Everything here is why the recording "just works".

- [ ] **Choose the flip pair** (the only real creative decision): run `~/.config/hypr/scripts/set-wall.sh ~/Pictures/wallpapers/<file>` per candidate, screenshot each, keep the pair with the strongest palette contrast:
  - Warm: `african-light.jpg` · `golden-hours.png` · `amber-island.jpg`
  - Cool: `glowing-green-dew.jpg` · `green_sea.jpg` · `deer_in_pine_forest.jpg`
  - End the video on the warm/peach scheme (brand-consistent end card)
- [ ] Stage workspaces: WS1 kitty (`fastfetch` + `btop`), WS2 chromium on a real project (+ editor), WS3/WS4 — each needs one clean visual story at 1080p
- [ ] DND on, `~/.zsh_history` cleared, WhatsApp/mail closed; notification test: `notify-send "HyprYoru" "Palette regenerated"`
- [ ] Terminal font 14pt+, cursor blink off ([[04-recording-checklist]])
- [ ] OBS: frozen settings + 2 scenes ([[03-production-stack]]); 20s test export first
- [ ] Optional: `ln -s ~/.config/hypr/scripts/set-wall.sh ~/.local/bin/set-wall.sh` so you can type just `set-wall.sh` on camera (use the full path everywhere below if you skip this)

## Shot list (silent pass first — narration is recorded later, over the footage)

| # | Time | What to capture |
|---|------|-----------------|
| 1 | 0:00 | **Cold open:** kitty fullscreen, fastfetch visible, warm scheme. Run `set-wall.sh` → cool. Capture the full repaint in one unbroken take. Then a clean static hold. (This take doubles as the money shot.) |
| 2 | 0:15 | **Workspaces:** `SUPER+1` → `2` → `3` → `4`, linger 2–3s each. Bonus: `SUPER+grave` scratchpad toggle |
| 3 | 0:35 | **Launcher:** `SUPER+Space` → type `kit` → Enter |
| 4 | 1:00 | **Terminal:** fresh kitty — `fastfetch`, then `btop` (tmux split if it looks good) |
| 5 | 1:20 | **Notifications:** `notify-send` pops → `SUPER+SHIFT+N` panel open/close |
| 6 | 1:40 | **The flip — 3 takes:** (a) `set-wall.sh --pick` → rofi list → Enter (b) `SUPER+SHIFT+W` random flip (c) cool → warm. Close-ups: Waybar strip, kitty mid-repaint, SwayNC open during a flip |
| 7 | 2:10 | **Dev corner:** `SUPER+B` browser on a real project, nvim on a real repo — 15s of genuine interaction, not posing |
| 8 | 2:40 | **Close:** 30s static hold on final rice (reused for end screen — [[04-recording-checklist]]) |

## Narration (record after; ≈220 words ≈ 2:40 speaking)

> **(0:15)** "Hey — I'm Elisha. This is HyprYoru, my Arch plus Hyprland desktop. I built every piece of it, and everything you're about to see runs from the keyboard."
>
> **(0:35)** "Super plus Space opens the launcher. I type two letters, and there's my terminal."
>
> **(1:00)** "Home base — system stats on the left, fetch on the right, and tmux when things get real."
>
> **(1:20)** "Notifications drop in here, themed to match. Super plus Shift plus N opens the whole command center."
>
> **(1:40)** "But here's my favorite part. One command — set-wall. It reads the new wallpaper, generates a color palette from it, and repaints the entire system. The bar. The terminal. The notifications. The launcher. Two seconds ago this desktop was gold. Now it's forest. Same command — completely different world."
>
> **(2:10)** "And when I'm not ricing? I'm building. This second workspace is where the full-stack projects happen — real code, real products, learning in public."
>
> **(2:40)** "Everything you saw is open source — HyprYoru, on my GitHub, link below. Next video: how the whole thing works, module by module. Subscribe if you want your Linux to look like this — and I'll see you there."

## Edit notes

Kdenlive mechanics: [[07-first-video-walkthrough]].

- Cut every 10–15s; rhythm: fullscreen → zoom → flip
- **Text overlays:** keybind chips (`SUPER + SPACE`, `SUPER + ⇧ + N`, `SUPER + 1–4`), the `set-wall.sh` command, one mini-caption on the flip: *"reads wallpaper → builds palette → repaints every app"*
- Title card at 0:08: `夜 DotYoru` + "DESK TOUR 2026"
- Music: one ambient/synth track, up in the cold open, ducked under voiceover
- If the `SUPER+SHIFT+W` take ends up as the main flip, change the VO line to "one keybind"
- Export `01-desk-tour_1080p60.mp4` → `~/Videos/hypryoru/export/01-desk-tour/`, −14 LUFS / −1 dB peaks, commit hash to `01-desk-tour.txt` ([[04-recording-checklist]])

## Final publish package (2026-10-20)

Final cut: **6:34** — one continuous take, single hard cut at 4:53.5. Master: `~/Videos/hypryoru/export/01-desk-tour/01-desk-tour_1080p60.mp4` (1080p60, −14.4 LUFS / −0.6 dBTP, faststart). Thumbnail: `01-desk-tour-thumb.png` beside it (copy in `~/Studio/yt-assets/`).

**Title:** `One Command Repaints My Entire Linux Desktop (Arch + Hyprland Desk Tour)`

Alternates: `I Built This Entire Linux Desktop. Here's the Tour.` · `My Hyprland Desk Tour — Recorded in One Take`

**Description (paste-ready):**

```text
One command — and my entire Linux desktop repaints: the bar, the terminal, the notifications, the launcher. This is HyprYoru — my Arch + Hyprland rice, recorded live in one take. No fake demos.

Chapters
0:00 Intro
0:10 The desktop — fastfetch
0:46 App launcher
1:10 Notifications
1:22 One command — whole desktop repainted
3:00 Dev corner — YoruNeovim
4:28 Pick any wallpaper
5:28 Final look

HyprYoru (the rice): https://github.com/ae-orlando/HyprYoru
YoruNeovim (editor): https://github.com/ae-orlando/YoruNeovim
Everything else: https://github.com/ae-orlando

The stack
- Arch Linux + Hyprland (Lua config)
- Waybar · Rofi · SwayNC · Kitty + zsh
- Editor: YoruNeovim (LazyVim)
- Theming: matugen — one wallpaper generates the palette for every app

Subscribe for the build series — next: how the whole system works, module by module.

#Hyprland #ArchLinux #LinuxRice #Dotfiles #Neovim
```

**Pinned comment:** *"Which part should I break down first — the Waybar, the launcher, or the wallpaper engine?"* (comment mining, [[05-publishing-and-sustain]])
