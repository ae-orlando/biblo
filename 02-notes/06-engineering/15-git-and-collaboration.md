# Git and collaboration — preserve work while changing it

> Expanded course: [[git-learning-path]] and its deliberate local workflow exercise. This page remains a compact reference; Git is not tied to the old authentication project. The author does not initialize a repository, commit or publish anything on your behalf.

## Outcome and boundary

Explain working tree, index and commits; make a focused change, review it and resolve a conflict without discarding unrelated work. The rebuild does **not** initialize a repository, commit files, contact remotes or publish the vault. Commands here are learner exercises for a separately chosen disposable repository.

## Mental model

The working tree is current files. The index stages the next snapshot. A commit records a tree, parents and metadata. A branch name points to a commit; HEAD usually names the checked-out branch. Git does not automatically back up untracked/ignored files or prevent secrets being committed.

Read-only orientation in an existing learner repository:

```bash
git status --short
git diff
git diff --cached
git log --oneline --decorate -5
```

Inspect changes before staging. A good commit captures one coherent, reviewed change; a conventional subject prefix is optional, not proof of professional collaboration.

## Deliberate learner exercise

After explicitly choosing/creating your own disposable repository:
1. Track a tiny parser and tests. Make the test fail, implement the fix and review the diff.
2. Stage only the intended source/test changes, inspect the staged diff, then commit.
3. On two branches, change the same behavior differently. Merge in the disposable repository, inspect conflict markers, decide the intended contract and rerun tests before completing the merge.
4. Revert a committed behavior change and explain why revert adds history while reset moves a reference and can affect index/worktree depending on mode.
5. Review a change as if submitted by a colleague: identify correctness, missing tests and unclear requirements, not only formatting preferences.

Do not use hard reset, checkout-discard, clean or force-push as an unexplained repair. A clean status does not prove no data was lost. Use an appropriate backup before risky operations and preserve other people's changes.

## Safety and completion

Keep real .env files, credentials, backups, runtime databases and downloaded tools out of a published repository. A gitignore rule does not remove already tracked data or history. Rotate exposed secrets rather than merely deleting the latest line. This vault currently relies on its verified local snapshot, not on an assumed Git history.

Completion evidence: reviewed diffs, conflict explanation, passing relevant tests and a justified revert in your learner repository. No remote account or PR publication is required; a written local review can demonstrate the review skill.

Sources: [Git documentation](https://git-scm.com/docs), [Pro Git](https://git-scm.com/book/en/v2).
