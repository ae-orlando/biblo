---
created: 2026-11-13
updated: 2026-11-13
---

# 10 Video 3 — Dynamic Theming Engine

Next upload after the zoxide guide. **Story + walkthrough, 10–12 min**, Module Guide / A-pillar. Working title: **How I Made Dynamic Theming Actually Reliable (Arch + Hyprland)**.

The video is not "install matugen". It is the coordination layer: one entry point, one generated palette, journaled batch publish, graceful reloads, rollback, and crash recovery. Source of truth for claims: `~/Dev/dotfiles/docs/matugen.md` and `hyprland/scripts/palette.py`.

Storage: `~/Videos/hypryoru/{raw,narr,export,thumb,projects}/03-dynamic-theming/`
Master: `export/03-dynamic-theming/03-dynamic-theming_1080p60.mp4` + `03-dynamic-theming-thumb.png`
Pinned commit: `export/03-dynamic-theming/03-dynamic-theming.txt`

## Locked decisions

- **Format:** story + walkthrough, one hard-parts code beat, no full `palette.py` read-through.
- **Hero pair:** cool `mystical-night-in-town.jpg` → warm `3d-tech.jpg`; end on warm for the brand close.
- **Toggle:** shoot light/dark on both wallpapers, choose the stronger take in edit.
- **Code beat:** latest-request-wins, validation + rollback, login recovery, backdrops.
- **Failure demo:** shot 12 only if a real broken-template rollback stages safely. No fake error screen.
- **Next-video line:** Waybar that consumes these colors. Swap the spoken line if the owed HyprYoru deep-dive ships first.

## Palette pre-test (2026-11-13)

Run through a temporary matugen config, not the live desktop. `scheme-tonal-spot`, contrast 0.

| Wallpaper | Mode | Primary | Surface | Read |
|---|---|---|---|---|
| `mystical-night-in-town.jpg` | dark | `#8ad6b7` | `#0f1512` | Cool green/teal, strong mid-tone separation |
| `mystical-night-in-town.jpg` | light | `#1a6b52` | `#f5fbf6` | Clean light mode, good contrast |
| `3d-tech.jpg` | dark | `#ffb692` | `#1a120e` | **Exact brand peach on brand dark** |
| `3d-tech.jpg` | light | `#8d4e2b` | `#fff8f6` | Warm light mode, usable |

The dark-palette concern is resolved: `3d-tech.jpg` maps to `#FFB692` on `#1A120E`, which is the channel palette. It is the correct final frame and thumbnail side.

## Pre-flight

- [ ] Confirm zoxide video is live (note 09 still says "awaiting upload")
- [ ] Pin commit at start: `git -C ~/Dev/dotfiles rev-parse --short HEAD` → currently `c7894be`, tree clean
- [ ] Freeze dotfiles during capture; re-pin after the last config change
- [ ] Run `set-wall.sh` for both hero wallpapers once, screenshot both, confirm the live palette matches the pre-test
- [ ] Stage WS1 Kitty (`fastfetch` + `btop`), WS2 nvim on `~/Dev/dotfiles`, WS3 SwayNC + Rofi, WS4 browser
- [ ] DND on, notifications paused, mail/chat closed, `~/.zsh_history` swept
- [ ] Terminal 14pt+, cursor blink off, keycast on
- [ ] OBS: 2560×1440 canvas → 1080p60, CQP 18, mic + desktop separate tracks; 20s test export
- [ ] Test both toggle directions; note which wallpaper reads better in light mode

## Shot list (silent pass first)

| # | Script time | What to capture | Notes |
|---|---|---|---|
| 1 | 0:00 | **Cold open:** start on `mystical-night-in-town`, full rice with fastfetch + btop. Run `set-wall.sh ~/Pictures/wallpapers/3d-tech.jpg` → full repaint in one unbroken take. Hold 5s | 3 takes; the money shot and the Short |
| 2 | 0:20 | **Toggle:** `~/.config/swaync/scripts/toggle-theme.sh` on `3d-tech`, then same on `mystical-night`. Capture Waybar, Kitty, SwayNC, Rofi | 2 takes each; pick in edit |
| 3 | 0:40 | **Problem B-roll:** SwayNC open during a flip; Rofi open during a flip; close-up of Waybar strip and Kitty mid-repaint; hyprlock lock → hold 2s → unlock (separate take) | No fake broken state. If OBS cannot capture the lock surface, show the generated hyprlock files instead and cut "lock screen" from the hook |
| 4 | 1:10 | **Workspace pass:** nvim on `~/Dev/dotfiles`, btop, browser | 2–3s each |
| 5 | 2:00 | **Pipeline proof:** terminal run of `set-wall.sh` with `time`; show output line | Diagram added in edit |
| 6 | 2:40 | **State files:** `cat ~/.cache/matugen/current-wallpaper`, `current-mode`, `jq . ~/.cache/matugen/committed.json`, `ls ~/.cache/matugen/transactions` | Zoom callouts |
| 7 | 3:20 | **Template map:** `nvim ~/.config/matugen/config.toml`, scroll the 13 template entries | Keycast on |
| 8 | 3:50 | **Split view:** `matugen/templates/waybar-matugen.css` ↔ `~/.config/waybar/colors/matugen.css`; show generated header with wallpaper path | Zoom to 4x if needed |
| 9 | 5:00 | **Consumers:** Waybar `@import` lines, Kitty include, Rofi `colors.rasi`, SwayNC import, btop theme, Spicetify color.ini; then the toggle command | Fast cuts, 2–3s each |
| 10 | 7:00 | **Hard-parts code beat:** `nvim palette.py` around `request()`, `render()`, `publish()`, `reload_consumers()` | Highlight id checks, validation, single reload pass |
| 11 | 7:45 | **Recovery proof:** `python3 ~/.config/hypr/scripts/palette.py recover`; show journal dir and `committed.json` | Clean run, no fake crash |
| 12 | 8:30 | **Optional real rollback:** break one template in a throwaway copy, run `set-wall.sh`, show validation error + wallpaper restore, restore template, re-run | Only if it stages cleanly |
| 13 | 9:45 | **Limits:** Firefox toolbar / Electron app / Steam next to a themed app | Honest comparison |
| 14 | 10:45 | **Final hold:** `3d-tech` rice, static 25–30s for end screen | Reuse for thumbnail |

## Narration (record after footage, ~150 wpm)

Current script is ~1,400 words ≈ 9:20 at 150 wpm; with command beats and holds, target cut **10:30–11:30**. One take, punch-ins only.

> **(0:00)** "One wallpaper. Thirteen generated files. The bar, the terminal, notifications, the launcher, btop, the lock screen — all repaint together. And if a render fails halfway, the old theme comes back.
>
> This is the theme engine behind HyprYoru, my Arch plus Hyprland desktop. Right now it's on this teal night street. One command, and it's this red and black tower — and the whole desktop follows. Same wallpaper, and I can flip light to dark without touching the image.
>
> This isn't a matugen install guide. Matugen is one piece. This is the coordination layer that makes dynamic theming actually reliable."

> **(0:40)** "Most dynamic theming setups do the easy twenty percent. They recolor the bar and the terminal, maybe the launcher, and call it done. Then you change the wallpaper and you get the halfway state: new background, old colors. The bar reloads before the palette is written. Rofi still shows yesterday's blur. The lock screen doesn't match at all. Change wallpapers twice quickly and the first render can land after the second, so your desktop ends up with colors from an image you already left. And if a template is broken, you find out after half your apps have already reloaded.
>
> None of that is a matugen problem. It's a coordination problem. So the system follows three rules. One command owns the whole change. Every consumer reads from one generated palette. And nothing goes live until every file is valid. Everything else in this video is how those three rules are enforced."

> **(2:00)** "Here's the whole pipeline. `set-wall.sh` is a thin wrapper around `palette.py`. Four phases: transition, render, publish, reload.
>
> Phase one: transition. `awww` starts a two-second center transition immediately. Matugen doesn't touch the wallpaper — `config.toml` has `set = false`. That matters. If matugen owned the image, you'd get a race between the wallpaper and the colors. The transition starts first, and the palette render has two seconds to catch up. If the awww daemon isn't ready, the command fails before changing anything.
>
> Phase two: render. The coordinator reads your live matugen config and builds an isolated copy. Same templates, same scheme — tonal spot, contrast zero — but every output goes to a temporary directory, and the per-template post-hooks are disabled. That's important: you don't want Waybar reloading halfway through a batch. The render is disposable until it passes validation.
>
> Phase three: publish. Every output has to exist, be non-empty, contain no unresolved template expressions, and any JSON has to parse. If one file is broken, nothing is published. Then the batch goes through a journal. New files and backups are flushed to disk before any rename. Only the latest request can publish, so a slow render from two wallpapers ago gets thrown away instead of overwriting the new one.
>
> Phase four: reload. One pass, after all files have landed: Hyprland, Waybar, SwayNC, Kitty, btop, Spicetify. Each gets a graceful signal once. Not kill and restart. Signals.
>
> Under all of it is a state directory: current wallpaper, current mode, committed dot json. That's how the system knows what it's actually showing, not what it intended to show.
>
> On the template side, twelve templates become thirteen files. Hyprland borders, hyprlock, Waybar, SwayNC, Kitty, Rofi, GTK three and four, Qt6CT, btop, Spicetify, an opt-in Neovim palette, and shell colors for eza and fzf. `config.toml` is the source of truth. Generated files are gitignored — edit an output and the next wallpaper wipes it. Fix the template."

> **(5:00)** "Let's look at one consumer. Waybar's stylesheet imports `colors/matugen.css` first, and the rest of the CSS uses semantic names — `bg0`, `fg`, `accent`, `danger` — instead of hard-coded hex. The template maps Material roles onto those names. Primary becomes accent. Surface becomes the bar background. Error becomes danger. On-surface variants handle text. Because the names are semantic, the stylesheet never changes when the palette does.
>
> Here's the generated file header. It records the exact wallpaper it came from. That's your proof, and it's the first thing to check when the colors look wrong.
>
> Kitty works the same way: a generated theme file included from `kitty.conf`. Rofi imports `shared/colors.rasi`. SwayNC imports `matugen/colors.css`. GTK gets `colors.css`. Qt gets a color scheme. btop gets a theme. Spicetify gets a `color.ini`. The shell gets a generated snippet for eza and fzf. None of them know about matugen. They only know the generated file.
>
> Why matugen instead of just extracting a few colors? Because Material roles give you a whole system: surfaces, containers, outlines, on-colors for contrast. You're not guessing which color goes on top of which. The scheme is tonal spot, contrast zero, and `prefer` is closest-to-fallback, so an odd wallpaper still produces a usable palette instead of something unreadable.
>
> Then there's the mode toggle. `toggle-theme.sh` calls the same coordinator with `toggle`. It doesn't re-animate the wallpaper. It re-renders the same image in light or dark, publishes the batch, and only an explicit toggle touches GTK preferences with `gsettings`. A wallpaper change doesn't silently change your GTK theme.
>
> Same wallpaper, same layout, two completely different moods. That's the part people feel."

> **(7:00)** "Three things make this reliable, and they're the parts I'd steal even if you never use matugen.
>
> First: only the latest request wins. Every request gets an id. Before rendering, and again before publishing, the coordinator checks `intent.json`. If the id doesn't match, it returns without publishing. So if I mash the wallpaper key, intermediate palettes get discarded. You never see a flash of a theme from a wallpaper you already left. It also means a slow render can't clobber a newer one — the newer request wins by design, not by luck.
>
> Second: failure rolls back. If matugen fails, or an output is empty, or a template has an unresolved expression, the exception path restores the previous wallpaper and resets the intent. If there's no previous successful wallpaper — first boot, for example — it can't roll back, and it tells you instead of pretending. The old theme stays on screen instead of half the desktop showing a broken palette.
>
> Third: crash recovery. Publishing uses a journal under `~/.cache/matugen/transactions`. New contents and backups are fsynced before the rename. If the power dies mid-publish, the next login runs `palette.py recover` before Waybar or SwayNC even start. Interrupted preparation means the old theme is untouched. Interrupted publication means the backups get restored. A committed batch keeps the new theme and cleans up. And recovery can itself be interrupted and repeated.
>
> The backdrops get the same treatment. Hyprlock's wallpaper and Rofi's blurred wallpaper are built during the two-second transition, but they're published only after that request's palette commits. So the lock screen can't be one wallpaper ahead of the colors.
>
> If you want to inspect the state, `palette.py recover` repairs files and state. It doesn't set a wallpaper or reload running apps.
>
> The tests run sandboxed — no desktop reloads — and cover the pipeline, GTK behavior, and recovery. That's how I can change this on camera without holding my breath."

> **(9:45)** "Now the honest part. This themes the things that read the generated files. Waybar, Kitty, SwayNC, Rofi, btop, hyprlock, GTK apps that respect the color scheme, Qt apps that use Qt6CT, Spicetify, and the shell. It does not magically theme everything. Firefox's toolbar doesn't repaint from your GTK color file. Most Electron apps ignore it. Steam has its own skinning. Neovim's palette is opt-in because `matugen.nvim` is a separate plugin. If an app doesn't expose its colors, no wallpaper engine can fix that — you need a per-app theme.
>
> So if you're building this yourself, don't start with more templates. Start with the three rules. One entry point. One palette. Publish only after validation. Add consumers after that. The pretty part is the easy part.
>
> The measure of a dynamic theme isn't how many colors it generates. It's whether the desktop ever looks broken while it changes. One command, one palette, one publish, one reload. That's the whole idea.
>
> Everything is in HyprYoru at the commit pinned below. The theming docs are in `docs/matugen.md`, and the tests run without touching your desktop."

> **(11:00)** "If you want the next layer, the next video breaks down the Waybar that consumes these colors — modules, workspaces, and the CSS that makes it look like this. Repo's below. Subscribe if you want your Linux to look like this. See you there."

## Edit notes

- Kdenlive profile 1080p60; save `projects/03-dynamic-theming/03-dynamic-theming.kdenlive`
- Cut every 10–15s: fullscreen desktop → zoomed config → result. Pattern interrupt at 0:40.
- Build one pipeline diagram in brand palette: peach `#FFB692` on `#1A120E`, GoMono Nerd Font Mono. Nodes: wallpaper → awww → matugen → validate → journal/publish batch → one reload pass.
- Text chips for commands: `set-wall.sh --pick`, `toggle-theme.sh`, `palette.py recover`, `~/.config/matugen/config.toml`
- Callouts: `13 outputs`, `latest request wins`, `rollback`, `fsync + journal`
- No intro logo. No goodbye. End on the result frame.
- Music: one ambient/synth bed, up in the cold open, ducked under VO.

## Thumbnail

1280×720, 50/50 split of the same layout in two palettes:
- Left: `mystical-night-in-town` rice (teal)
- Right: `3d-tech` rice (peach/red)
- Text: `1 WALLPAPER` top, `EVERY APP` bottom; peach `#FFB692`, dark `#1A120E` stroke 6–8 px, 90–100 px
- Fonts: `/usr/share/fonts/TTF/GoMonoNerdFontMono-Bold.ttf`; `夜 DotYoru` chip bottom-left with Noto Sans SC
- Save `export/03-dynamic-theming/03-dynamic-theming-thumb.png` + copy to `~/Studio/yt-assets/` with a new name; never overwrite an existing asset

## Publish package (draft — re-pin chapters after QA)

**Title:** `How I Made Dynamic Theming Actually Reliable (Arch + Hyprland)`

Alternates: `I Built a Theme Engine for My Linux Desktop` · `One Wallpaper, 13 Files: Inside My Dynamic Theming Pipeline`

**Description:**

```text
One wallpaper changes thirteen generated files — the bar, terminal, notifications, launcher, btop, lock screen, GTK/Qt, and Spicetify. Here's the coordination layer that keeps the desktop from looking broken while it changes: validated batch publish, rollback, and crash recovery.

Chapters
0:00 One wallpaper, whole desktop
0:40 Why dynamic themes look broken
2:00 The pipeline
3:20 The template map
5:00 Inside one template
7:00 Races, rollback, recovery
9:45 What doesn't follow the theme
10:45 Repo and next

HyprYoru (the rice): https://github.com/ae-orlando/HyprYoru
YoruNeovim (editor): https://github.com/ae-orlando/YoruNeovim
Everything else: https://github.com/ae-orlando

The stack
- Arch Linux + Hyprland (Lua config)
- matugen — wallpaper-derived Material palette, scheme-tonal-spot
- palette.py — isolated render, journaled batch publish, rollback, recovery
- Waybar · Rofi · SwayNC · Kitty · btop · GTK/Qt · Spicetify
- Docs: docs/matugen.md in the HyprYoru repo

Subscribe for the build series — next: the Waybar that consumes these colors.

#Hyprland #ArchLinux #LinuxRice #Matugen #DotYoru
```

- [ ] Chapters are draft only; derive exact boundaries from the QA sweep
- [ ] Re-check all links before pasting (verified 200 on 2026-11-13)
- [ ] Pinned comment: *What breaks first when you theme your setup — the bar, the launcher, or the lock screen?*

## Upload checklist

- [ ] Upload master + thumbnail; not made for kids
- [ ] Playlist: **Module Guide**, autoplay on
- [ ] Unlisted → full watch (chapters parse, audio, first frame) → Public
- [ ] Auto-captions, then fix: HyprYoru, Hyprland, matugen, palette.py, Waybar, SwayNC, Rofi, btop, hyprlock, awww, Qt6CT, gsettings, fsync
- [ ] End screen on the final hold; one Subscribe element
- [ ] Publish → pin the question comment → reply to early comments
- [ ] After publish: add video URL here, update `00-index.md` + `02-content-system.md`

## Publish log

- (awaiting record)
