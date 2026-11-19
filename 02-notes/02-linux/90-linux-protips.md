---
created: 2026-10-08
updated: 2026-10-21
---

# Linux Protips

> **Editor qualification, 2026-10-21; not fabricated experience.** Dated entries remain historical. checkupdates uses a separate temporary package database rather than “no database syncing at all”; it avoids refreshing the normal database for a partial upgrade. Public SSH keys need not share private-key modes. Inspect history expansion before adding sudo and prefer a precise owned PID to broad matching. Current assessed practice is in [[linux-learning-path]].

Living list. Append-only — one entry per trick you actually used. Promote from `06-journal/` when used twice. Newest on top.

How to add:
```md
## YYYY-MM-DD — short title
Context: what you were doing
Run: `exact command`
Why: one line
```

---

## 2026-10-08 — Back to previous dir
Context: bouncing between Notes and /etc.
Run: `cd -`
Why: `OLDPWD` toggle, faster than retyping path.

## 2026-10-08 — Make dir tree + jump into it
Context: scaffolding `02-linux/` notes.
Run: `mkdir -p a/b/c && cd $_`
Why: `$_` = last arg of previous command.

## 2026-10-08 — Find PIDs without self-match
Context: `ps aux | grep sshd` shows grep itself.
Run: `pgrep -af sshd`
Why: never matches itself, `-a` shows full cmdline, scriptable (exit 1 = no match).

## 2026-10-08 — See all listening ports + owners
Context: "what's on 5432?"
Run: `sudo ss -tulpn`
Why: `-p` needs sudo for other users' procs; bare `ss` hides them.

## 2026-10-08 — Search service logs without piping
Context: sshd failures.
Run: `journalctl -u sshd --grep=Failed -e`
Why: `--grep` preserves pager/colors vs `| grep`.

## 2026-10-08 — Safe pending-update check
Context: haven't updated in weeks, afraid of `Sy`.
Run: `checkupdates | head -30`
Why: lists pending without syncing DB (no partial-upgrade risk). From `pacman-contrib`.

## 2026-10-08 — List .pacnew before they rot
Context: post-`Syu` cleanup.
Run: `find /etc -name '*.pacnew' -o -name '*.pacsave'`
Why: merge with `DIFFPROG=nvim\ -d pacdiff -s`.

## 2026-10-08 — Rerun last command with sudo
Context: `pacman -Syu` denied.
Run: `sudo !!`
Why: `!!` = previous history line (interactive only).

## 2026-10-08 — Which package owns a file (and reverse)
Context: "what installed this config?"
Run: `pacman -Qo /etc/pacman.conf` / `pacman -Ql ripgrep | head`
Why: `-Qo` file→pkg, `-Ql` pkg→files. Remote: `pacman -F`.

## 2026-10-08 — Disk full? Biggest dirs first
Context: `/` filling up.
Run: `df -h; du -sh /* 2>/dev/null | sort -hr | head`
Why: `df` = filesystems, `du -sh` = sizes, `2>/dev/null` hides perm noise. Cache culprit? `paccache -d` dry-run.

## 2026-10-08 — Reattach tmux after close
Context: ssh dropped mid-edit.
Run: `tmux a -t notes || tmux new -s notes`
Why: attach or create; `Ctrl-b d` detaches cleanly.

## 2026-10-08 — Exact mode + owner in one line
Context: SSH key `too open` error.
Run: `stat -c '%a %U:%G %n' ~/.ssh/id_*`
Why: expect `600 orlando:orlando`. Fix: `chmod 600`.

---

## Related

- [[00-linux-introduction|Linux Introduction]]
- [[70-linux-shell-workflow|Shell Workflow]]
