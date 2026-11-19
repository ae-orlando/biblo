---
created: 2026-10-08
updated: 2026-10-21
---

# Bash Protips

> **Editor correction, 2026-10-21; not a new learner experience.** Historical entries below are retained. An `a && b || c` dry-run wrapper can execute c if logging fails; use an explicit if. Traps do not always run (SIGKILL/power loss), TERM cleanup can return without exiting, SC2086 is not “always the bug,” and PATH inclusion is configuration-dependent. Follow [[10-robust-bash-scripts]], [[10-bash-traps-jobs]] and [[practice-catalog]] for corrected contracts. Host/AUR commands are VM/reference material.

Living list. Append-only — one entry per trick you actually used. Promote from `06-journal/` when used twice. Newest on top.

How to add:
```md
## YYYY-MM-DD — short title
Context: what you were doing
Run: `exact command`
Why: one line
```

---

## 2026-10-08 — Preview destruction before running
Context: installer would `pacman -S` 40 packages.
Run: `./install.sh --dry-run` (with `run() { (( DRY_RUN )) && log "DRY: $*" || "$@"; }`)
Why: every destructive call goes through `run`.

## 2026-10-08 — Strict mode caught a pipe failure
Context: `download | install` silently passed with broken download.
Run: `set -euo pipefail` at top (verified: `false | true` exits 1 with it, 0 without).
Why: pipeline = last non-zero. Without it only last command counts.

## 2026-10-08 — Lint before debugging
Context: chasing a space-splitting bug for 20 min.
Run: `shellcheck install.sh; shfmt -i 2 -ci -bn -d install.sh`
Why: SC2086 (unquoted `$var`) is always the bug. Install: `sudo pacman -S shellcheck shfmt`.

## 2026-10-08 — Idempotent package line
Context: re-running installer reinstalled everything.
Run: `pacman -Qq hyprland &>/dev/null || sudo pacman -S --needed --noconfirm hyprland`
Why: `-Qq` quiet check + `--needed` = re-run is no-op.

## 2026-10-08 — AUR helper pick + non-interactive answers
Context: `yay` hung on diff menu in script.
Run: `"$HELPER" -S --needed --noconfirm --noremovemake --answerclean All --answerdiff None pkg`
Why: `--noconfirm` alone doesn't answer clean/diff menus. Never `sudo yay`.

## 2026-10-08 — Safe temp dir that cleans itself
Context: cloning AUR pkgs to /tmp.
Run: `tmp=$(mktemp -d); trap 'rm -rf -- "$tmp"' EXIT INT TERM`
Why: single-quoted trap expands at exit; always cleans, even on Ctrl-C.

## 2026-10-08 — Stow dry-run before linking dotfiles
Context: afraid `stow` would overwrite `~/.config/hypr`.
Run: `stow -n -v -t ~ hypr` (then `stow -t ~ hypr`, `stow -R` to restow, `stow -D` to unlink)
Why: `-n` previews; conflicts abort safely, never delete. `--adopt` pulls live files INTO repo.

## 2026-10-08 — Colors only on tty
Context: log file full of `^[[31m`.
Run: `if [[ -t 1 ]]; then RED=$'\e[31m'; RST=$'\e[0m'; else RED=''; RST=''; fi`
Why: escapes garble pipes/logs.

## 2026-10-08 — Check service state quietly in scripts
Context: noisy `systemctl is-enabled` output.
Run: `systemctl is-enabled --quiet sddm || sudo systemctl enable sddm`
Why: `--quiet` = exit code only (0 yes). Same for `is-active`.

## 2026-10-08 — Place script on PATH properly
Context: `./install.sh` only works from one dir.
Run: `install -m755 install.sh ~/.local/bin/my-setup`
Why: creates + chmods at once; `~/.local/bin` is Arch PATH after relogin.

---

## Related

- [[00-bash-basics|Bash Basics]]
- [[30-script-workflow|Script Workflow]]
- [[90-linux-protips|Linux Protips]]
