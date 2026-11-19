---
created: 2026-10-19
updated: 2026-10-19
---

# 07 First Video Walkthrough

Record silent → narrate → razor-cut → upload. Click-by-click version of [[03-production-stack]] + [[04-recording-checklist]] + [[05-publishing-and-sustain]] for someone who has never recorded or published a video. Settings are decided once and frozen — never tweaked per video.

## 0 — Tools (once)

```bash
sudo pacman -S kdenlive pavucontrol easyeffects   # skip anything already installed
```

- obs-studio + Wayland capture chain: already set up ([[03-production-stack]])
- kdenlive — the editor ("where do I edit")
- pavucontrol — mic level check
- easyeffects — frozen audio chain ([[03-production-stack]])

Mic check: pavucontrol → Input Devices → speak → bar must move. Same mic + same distance every session.

## 1 — OBS setup (once, ~15 min)

Exact values (canvas, output, fps, CQP, tracks) are in [[03-production-stack]] — copy once, then never open Settings again. Mechanics:

1. `+` → **Screen Capture (PipeWire)** → pick monitor → tick *Restore Token* so the portal only asks once.
2. `+` → **Audio Input Capture** → mic.
3. `+` → **Audio Output Capture (PipeWire)** → desktop sound, own track.
4. Scenes: 1 fullscreen desktop, 2 zoomed terminal (4x) — per [[03-production-stack]].
5. Recording format `.mkv` + remux to mp4 after (File → Remux Recordings). A crash never kills an MKV.
6. Test export: record 20 s → not black → mic peaks −12 to −6 dB, never red.

Hyprland: keep OBS on workspace 10, record workspace 1 — OBS never appears in frame. Black picker → portal restart command in [[03-production-stack]].

## 2 — Record

Pre-flight = [[04-recording-checklist]] (DND, secrets, fonts, disk). Then:

1. **Silent pass:** 10 s static result shot → full run-through without talking (edit → `hyprctl reload` → before/after) → 5 s close-up per changed hunk → break test.
2. **Narration:** separate session over the footage. 150 wpm; beats (hook → 3 outcomes → walk → pitfall → close) in [[04-recording-checklist]].
3. Flub a line? Pause 2 s, repeat it — cut the bad take later. Never restart the session.

## 3 — Edit in Kdenlive (video #1 ≈ 45 min)

Razor + delete is 95% of editing; the rest is polish.

1. New Project → profile `1080p 60fps` (match OBS output).
2. Drag `~/Videos/hypryoru/raw/NN-slug/` into the Project Bin → drag to timeline; narration track above footage.
3. Cut loop: move the playhead → `Shift+R` cuts the clip there (or toggle the razor with `X` and click to split) → select junk → `Delete` → drag the gap closed. Keep the fullscreen → zoom → reload rhythm every 10–15 s ([[02-content-system]]).
4. On-screen text for every command/keybind shown.
5. Audio: use the frozen chain output ([[03-production-stack]]); export −14 LUFS, peaks −1 dB.
6. Captions: auto-generate → fix command typos → keep the SRT for upload.
7. Render MP4 (H.264) → `~/Videos/hypryoru/export/NN-slug/NN-slug_1080p60.mp4` + `NN-slug-thumb.png` → write the pinned commit hash to `export/NN-slug.txt` ([[04-recording-checklist]]).

No intro logo, no goodbye — end on result + 1 spoken next-video link ([[02-content-system]]).

## 4 — Publish in Studio (~20 min)

1. studio.youtube.com → CREATE → Upload → MP4 from `export/`.
2. Title: [result + scope] — formula in [[05-publishing-and-sustain]].
3. Description: paste [[youtube-first-video-description]] → replace placeholders with real timestamps + commit link + `install.sh` command.
4. Thumbnail: rice or fastfetch shot + ≤3 words (formula in [[03-production-stack]]). A/B via CTR after 48 h.
5. Playlist per series ([[02-content-system]]). Chapters: description timestamps, first one `0:00`.
6. Audience: not made for kids. Visibility: **Unlisted** → watch it once yourself → **Public**.
7. After publish: end screen (1 spoken recommendation), pin a question comment — comment mining feeds the next Build Log ([[05-publishing-and-sustain]]).

## 5 — Short (1 per long video)

Studio → your video → **Clip** button → mark 20–40 s over the result demo → share to Shorts. Zero re-editing. Cap: 1 long = 1 Short ([[02-content-system]]).

## Time budget

| Video | End-to-end |
|-------|------------|
| #1 | 3–5 h — everything is new |
| #2–3 | ~2 h |
| #5+ | ~1 h |

Batch: record 2 one day, edit on another — never both same day ([[05-publishing-and-sustain]]). Follow [[06-90-day-plan]]: bank videos 1–3 unreleased, fix workflow gaps, then ship weekly. Rough is fine — shipped beats perfect.
