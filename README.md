# Yoru Notes – my personal note system

A minimal Neovim‑linked Obsidian vault for capturing thoughts, journaling, and project notes. Everything is driven by `lua/config/notes.lua` and `90-tools/notes.py`.

---
## Quick start

```bash
# Ensure the vault exists at ~/Documents/Notes
# (it is already git‑initialized and has the templates)

# Open Neovim with the yoru app name
NVIM_APPNAME=yoru nvim
```

### Creating a new note
- **In Neovim**: `<leader>mn` → type a title → file appears in `00-inbox/YYYY‑MM‑DD‑<slug>.md`.
- **From the shell**: `note "My new note about foo"` does the same.

### Note types (pick one after `<leader>mt`)

| Type | What it does | Advantage |
|------|--------------|-----------|
| **Capture** | Quick inbox entry with auto‑dated filename | Instant capture, never lose an idea |
| **Journal: daily** | Opens `06-journal/YYYY/MM/DD‑dddd.md` (today + weekday) | One‑click daily reflection |
| **Journal: weekly** | Opens `06-journal/YYYY/YYYY‑Www.md` (ISO week) | Fast weekly review |
| **Concept** | Creates `02-notes/<track>/<slug>.md` using a concept template | Structured problem/mechanism/retrieval |
| **Evidence** | Creates `01-roadmap/evidence/YYYY‑MM‑DD‑<slug>.md` | Claims with artifacts, verification table |
| **Review** | Creates `01-roadmap/reviews/YYYY‑MM‑DD‑<slug>.md` | Closed‑note prompt, result tracking, next‑review date |
| **Project** (`<leader>mp` [‑‑repo <path>]) | Creates `04-projects/<slug>.md`; optional `repo:`/`remote:` front‑matter | Project doc that pulls in git info automatically |

### Opening in Obsidian
- `<leader>mo` sends `obsidian://open?vault=Notes&file=<relative>` – jump from Neovim to Obsidian (or vice‑versa).

### Finding / searching notes
- `<leader>mi` – Snacks picker on `00-inbox`
- `<leader>mf` – Snacks picker on the whole vault
- `<leader>mg` – Grep the vault

### Task capture
- `<leader>mT` → type a task → creates `00-inbox/YYYY‑MM‑DD‑task‑<type>‑<title>.md` with task front‑matter.

### Task next
- `<leader>mN` opens a bottom‑terminal showing `task next`.

### Vault health check
- `<leader>mv` or run `python3 90-tools/check-vault.py` from the vault root; exits 0 when templates, attachments, and git are clean.

### Zen mode (focus write)
- `<leader>mz` hides line numbers, sign column, fold column, status line; press again to restore exactly where you left off.

### Toggle rendered Markdown
- `<leader>mr` switches `RenderMarkdown` on/off in the current buffer.

---
## My daily rhythm

1. **New thought** – hit `<leader>mn`, type a title, the note lands in `00-inbox/YYYY‑MM‑DD‑slug.md`.  
2. **End‑of‑day filing** – review inbox items and move them into `01-roadmap/evidence/`, `01-roadmap/reviews/`, or delete.  
3. **Journal** – `<leader>mj` opens today’s page; add reflections, `![[image.png]]` for captures.  
4. **Weekly wrap‑up** – `<leader>mw` jumps to this week’s journal.  
5. **Concept / evidence / review** – choose the type after `<leader>mt`, give a title, and the appropriate template (front‑matter + sections) is auto‑generated.  
6. **Check vault health** – `<leader>mv` whenever something feels off.  
7. **Focus session** – `<leader>mz` for a distraction‑free write; press again to restore.

---
## Tips I actually use

- **Keep images small** – all PNGs/JPGs go into `attachments/`. The resolver first checks the note’s `attachments/` folder, then the vault root.  
- **Matugen palette** – my wallpaper is the single source of colour for Neovim, Waybar, Rofi, Kitty, Hyprland. If the palette ever drifts I run `yarn matugen-reload` (or the `:MatugenReload` command in Neovim).  
- **Image overlap** – if both the markdown source (`![[image.png]]`) and the rendered Kitty image appear on the same line, I add a blank line between the heading and the image, or set `wrap = false` in my personal `lua/config/options.lua`.  
- **Avoid the `gcm` zsh warning** – the zsh helper was renamed to `gcom`; I keep `gcom` for `git commit -v` and use `git checkout $(git_main_branch)` for the original alias.

---
## Checks

```bash
# From the vault root
python3 90-tools/check-vault.py   # exits 0 when everything is clean
```

---
*This README is a personal guide – it reflects my own workflow and preferences. Feel free to adapt the commands, key‑bindings, or templates to suit your own system.*
