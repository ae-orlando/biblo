---
created: 2026-10-16
updated: 2026-10-16
---

# 04 Recording Checklist

## Pre-flight (5 min)
- [ ] DND on, SwayNC popups paused
- [ ] Close mail/messages, clear secrets from `~/.zsh_history`, fastfetch, browser tabs
- [ ] Fixed test wallpaper, 1920x1080 workspace, scale 1x for readability
- [ ] Terminal font 14pt+, cursor blink off, keycast on
- [ ] `hyprctl reload` works, Waybar launch script works
- [ ] OBS: PipeWire source live, tracks mic+desktop separate, 60fps, disk space >20GB
- [ ] VM snapshot taken (for C-series)

## Record (silent)
1. 10s static result shot (for thumbnail + end screen hold)
2. Full run-through no talking: open config, edit, save, `hyprctl reload`, demo before/after
3. Close-ups: each changed hunk fullscreen 5s
4. Break test: reboot VM or kill bar, show recovery

## Narrate
Script beats (150 wpm, 900 words ~= 6 min):
- Hook (3 sentences): result + who it's for + time saved
- 3 outcomes list on screen
- Walk: file path spoken + shown, diff explained, reload proof
- Pitfall: 1 thing that breaks + fix
- Close: commit hash + next video name spoken over result frame

Record in one take, punch-in fixes only. No mouth clicks editing — gate handles it.

## Export
- [ ] Captions generated + corrected for commands
- [ ] Loudness -14 LUFS, peaks -1dB
- [ ] First frame = hook rice, last 20s = result hold for end screen
- [ ] Filename: `NN-slug_1080p60.mp4` + `NN-slug-thumb.png`
- [ ] Note pinned commit: `git -C ~/Dev/dotfiles rev-parse --short HEAD`
