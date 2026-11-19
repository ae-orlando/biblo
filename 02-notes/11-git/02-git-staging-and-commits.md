# Git 02 — stage a deliberate snapshot and review it

## Outcome

Distinguish working-versus-index and index-versus-HEAD differences, then commit only an intended coherent change. Prerequisite: Git's model. Practice: the staging phase of the local workflow exercise.

```bash
git status --short
git diff
git diff --cached
```

git diff normally compares unstaged work with the index; --cached compares the staged snapshot with HEAD. Adding a file stages its current version. Editing it afterward can leave both a staged change and a further unstaged change; a commit does not automatically include that later edit.

## Review before recording

In your disposable repo, stage named intended files rather than blindly adding the whole directory. git add -p can stage selected hunks when that produces a coherent/testable snapshot. Inspect the staged diff, run relevant checks and use a message explaining intent. A conventional feat/fix prefix is optional, not proof of useful commits.

A commit message does not guarantee the staged state matches the tested working state. When staging partial work, check what is actually being recorded. Do not accidentally include a real .env file, generated cache or unrelated person's changes.

git restore --staged PATH removes that path from the proposed snapshot without discarding its working-tree edits in the ordinary case. Plain restore of a working path has a different effect and can discard edits; inspect/help first instead of treating all restore commands as “undo safely.”

## Practice and transfer

The exercise creates HEAD limit 10, stages limit 20, then edits the working file to 25. Predict both diffs before running them, choose the final intended change and explain what the next commit contains. Save sanitized evidence outside the repo so it does not interfere with the clean-status checkpoint.

Then introduce two unrelated edits and record them as separately reviewed commits. Explain which test evidence applies to each snapshot and why a giant unrelated commit is harder to review/revert.

Sources: [recording changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository), [git diff](https://git-scm.com/docs/git-diff), [git add](https://git-scm.com/docs/git-add).
