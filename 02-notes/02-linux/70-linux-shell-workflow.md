---
created: 2026-10-08
updated: 2026-10-21
---

# Shell Workflow (bash/zsh, history, tmux)

> Outcome: identify the active interpreter and choose an appropriate startup scope without changing global configuration as a learning prerequisite. Use [[00-how-to-use-track]] for Bash semantics; shell/editor setup is optional and outside the vault rebuild.

## Mental model

Shell = REPL for OS: expands (`* ~ $VAR`), then runs. `bash` is Arch default. History + aliases + PATH save keystrokes. `tmux 3.7c` (installed here) keeps sessions alive after terminal/ssh closes. Prefix is `Ctrl-b`.

## Core commands

| Command | What it does | Example |
|---|---|---|
| `Ctrl-R` | reverse history search (fzf makes it fuzzy) | `Ctrl-R`, type `pacman` |
| `!! / !$ / !:2` | last cmd / last arg / nth arg | `sudo !!`, `cd !$` |
| `history` | list | `history \| tail -20` |
| `command -v / type` | resolve (preferred over `which`) | `command -v nvim; type ll` |
| `alias` | shortcut (shell-only, not scripts) | `alias ll='ls -lah'` |
| `export PATH` | search dirs | `export PATH="$HOME/.local/bin:$PATH"` |
| `source ~/.bashrc` | reload config | `source ~/.bashrc` |
| `tmux new -s / ls / a -t` | new / list / attach | `tmux new -s notes` |
| `fzf` | fuzzy picker | `fd -H . ~ \| fzf` |

Typical terminal behavior: Ctrl-C sends INT to the foreground process group; handlers may change its effect. Ctrl-D is an input/EOF convention, not a kill signal. Ctrl-Z typically stops the foreground group. Editor/terminal mode and keybindings can change these behaviors.

PATH goes in login files, not every `*rc` (avoids duplication): bash → `~/.bash_profile`, zsh → `~/.zshenv`, or portable `~/.config/environment.d/*.conf`. `~/.local/bin` is **NOT auto-added** on Arch — create + export manually:
```bash
mkdir -p ~/.local/bin
# in ~/.bash_profile (bash) or ~/.zshenv (zsh):
export PATH="$HOME/.local/bin:$PATH"
```

tmux essentials (prefix `Ctrl-b`): `c` new window, `%` / `"` vertical/horizontal split, `x` kill pane, `d` detach, `tmux ls` list, `tmux a -t notes` reattach, `tmux kill-session -t notes`, `tmux kill-server` all. `tmux-resurrect` is a **plugin** (AUR `tmux-resurrect` or TPM `set -g @plugin 'tmux-plugins/tmux-resurrect'`), not builtin.

## Arch note (this machine)

Historical setup observations are not a current inventory. Do not create/replace a shell configuration or change the login shell based on this old note. If deliberately configuring your own shell later, consult its startup-file documentation and preserve existing settings first:
```bash
chsh -l
sudo pacman -S zsh
chsh -s /usr/bin/zsh   # or /usr/bin/bash to revert
```
Bash configs: `~/.bashrc` (interactive) + `~/.bash_profile` (login). Zsh: `~/.zshrc` + `~/.zprofile`. Reload: `source ~/.bashrc` / `source ~/.zshrc`. With `fzf` installed (`extra/fzf`), enable its keybindings for fuzzy `Ctrl-R` / `Alt-C` dir-jump.

Starter `~/.bashrc`:
```bash
alias ll='ls -lah'
alias gs='git status -sb'
alias pac='sudo pacman -Syu'
alias upd='checkupdates | head -30'
export EDITOR=nvim
```

## Pitfalls

- Edited `*rc` but nothing changed = forgot `source`, or edited bash file while running zsh.
- `PATH="$PATH:."` globally = hijack risk — use `./run.sh` explicitly.
- Nested tmux (`tmux` inside `tmux`) doubles prefix — detach outer first or use `tmux -L other`.
- `!!` in scripts fails (history expansion is interactive-only) — use `$!` (last PID) / `$?` (exit code) instead.

## Try it

```bash
echo $SHELL; echo $PATH
command -v bash; type alias
history | tail -5
tmux new -s test   # Ctrl-b d to detach, then: tmux ls; tmux a -t test; tmux kill-session -t test
fd -H . ~/Documents | fzf
```

## Related

- [[20-linux-files-and-text|Files and Text]]
- [[90-linux-protips|Linux Protips]]

Sources: [Bash](https://wiki.archlinux.org/title/Bash), [Zsh](https://wiki.archlinux.org/title/Zsh), [environment variables](https://wiki.archlinux.org/title/Environment_variables). Check: explain configured login shell versus current interpreter and show that the Bash labs run explicitly without modifying rc files. environment.d applies to relevant systemd user-service environments, not universally to every login shell.
