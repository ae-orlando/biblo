---
created: 2026-10-16
updated: 2026-10-20
---

# 03 Production Stack

Voiceover + screen only. 2 scenes, frozen settings.

## Video capture — Hyprland/Wayland
You have: pipewire, wireplumber, `xdg-desktop-portal-hyprland`, `qt6-wayland`, obs-studio.

- OBS source: Screen Capture (PipeWire) only. Not XSHM.
- If black picker: `systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP` then `systemctl --user restart xdg-desktop-portal-hyprland`.
- Settings: canvas 2560x1440, output 1920x1080, 60fps, CQP 18, separate tracks mic/desktop.
- Quick inserts: `wf-recorder -g "$(slurp)" -f ~/Videos/insert.mp4` or `grim -g "$(slurp)" - | swappy -f -` for stills.
- Scenes: 1) Fullscreen desktop 2) Zoomed terminal (4x for config). Keystroke overlay on.

## Audio
USB dynamic mic (Samson Q2U / Fifine AM8) > condenser on Linux.
Chain: Pipewire -> pavucontrol -> EasyEffects (noise gate + compressor + de-esser). Export -14 LUFS. Freeze chain, don't tweak per video.
Record narration after footage. Closet/soft room, same mic distance every time.

## Editing
Kdenlive (fast) or DaVinci Resolve (better color). Preset: 1080p60 timeline, loudness normalize, auto-captions burned + SRT upload.
Cuts: silence strip, zoom punch every 10-15s, text overlay for commands/binds.

## Thumbnails + brand
Reuse matugen palette. Formula: rice screenshot + 3 words max + 1 arrow/circle. No face. Keep font fixed (GoMono Nerd Font Mono + Noto Sans SC for 夜).
fastfetch shot works for 80% of videos.

## Storage
`~/Videos/hypryoru/{raw,narr,export,thumb,projects}/NN-slug/`. Keep raw until published + 30 days. Pin dotfiles commit hash in `export/NN-slug.txt`. Always save the Kdenlive project to `projects/NN-slug/` — exports alone cannot be re-rendered.
