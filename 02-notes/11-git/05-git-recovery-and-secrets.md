# Git 05 — recovery without casually discarding work

## Outcome

Choose an undo strategy based on what must be preserved and what has been shared. Prerequisites: staging, commits and graph reasoning. Practice: the revert/ignore phase of the local workflow exercise.

## Different actions change different things

- Revert records a new commit reversing a specified change; it preserves the history of the original. Reverting merges has additional parent/semantic decisions—do not guess.
- Reset moves a reference and, depending on mode, can change the index/worktree. A hard reset can discard work; it is not the default way to “fix Git.”
- Restore can affect the index or working files depending on options. Know which version is being copied where.
- Stash temporarily records selected work; untracked/ignored files are not all included by default. It is not an offsite backup or proof every file is safe.
- Reflog records local reference movements for a limited lifetime. It can help locate commits, but expires/garbage collection and untracked work limit what it can recover.

Before risky operations, preserve valuable work and inspect status/diffs/graph. Never run a broad clean/reset/discard command just to satisfy a checker. In a real collaboration, preserve changes you did not make and coordinate history rewrites explicitly.

## Secrets and generated state

A .gitignore rule does not untrack an already tracked file or erase old commits. Removing a token from the latest version does not make the old token safe. Rotate/revoke real exposed credentials and follow an appropriate history-remediation/access policy.

For a web app, normally keep real .env values, local environments, caches, runtime databases, backups and private logs out of published source. Track reviewed dependency locks and safe .env.example names/placeholders where useful. Git ignore and HTTP public-file boundaries solve different problems.

## Practice and transfer

In the fake-data sandbox, commit a deliberately bad policy change, then revert that ordinary commit and explain the new graph. Add only a fake training .env to demonstrate ignore behavior; never use a real credential. The optional read-only checker verifies selected artifacts, not your recovery judgment.

Retrieve: which information cannot be recovered merely because a repository has commits? Why is a clean status compatible with having lost untracked work? When would reverting an ordinary commit be safer for shared history than moving a branch backward?

Sources: [git revert](https://git-scm.com/docs/git-revert), [git reset](https://git-scm.com/docs/git-reset), [git restore](https://git-scm.com/docs/git-restore), [gitignore](https://git-scm.com/docs/gitignore), [reflog](https://git-scm.com/docs/git-reflog).
