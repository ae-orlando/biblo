# Manual lab: deliberate local Git workflow

Prerequisites: [[git-learning-path]] units 01–03 and a terminal. Outcome: demonstrate staging, divergence, conflict resolution, ignore policy and a safe revert. **No commands below are executed by the vault rebuild. You choose to run them only in this new disposable fake-data repository.**

## 1. Create your own sandbox explicitly

From the vault root, only when ready:

```bash
mkdir -p 03-exercises/git/01-local-workflow/work
git init -b main 03-exercises/git/01-local-workflow/work/repo
cd 03-exercises/git/01-local-workflow/work/repo
git config user.name 'Training Learner'
git config user.email 'learner@example.test'
printf 'git-practice\n' > .vault-training
printf 'limit=10\n' > policy.txt
git add .vault-training policy.txt
git diff --cached
git commit -m 'Document default limit'
```

These settings are repository-local. Do not use a real token or initialize the vault root. Subsequent Git commands in phases 2–4 run inside this sandbox.

## 2. Prove the three versions differ

Write limit=20, stage policy.txt, then change only the working file to limit=25. Before running git diff and git diff --cached, predict each comparison against HEAD/index. Save sanitized outputs in an evidence note **outside repo/**.

```bash
printf 'limit=20\n' > policy.txt
git add policy.txt
printf 'limit=25\n' > policy.txt
git diff --cached
git diff
```

Choose/stage the intended final value 25, inspect the staged diff and commit it. Add a .gitignore containing .env, create only a fake .env (TRAINING_TOKEN=fake), commit the ignore rule but not .env. Explain why an already tracked secret would require more than this ignore rule.

```bash
git add policy.txt
git diff --cached
git commit -m 'Raise default limit'
printf '.env\n' > .gitignore
printf 'TRAINING_TOKEN=fake\n' > .env
git add .gitignore
git diff --cached
git commit -m 'Ignore local training settings'
```

## 3. Resolve real divergence

Create feature-limit from current main. On that branch change policy.txt to limit=30 and commit. Switch to main, change it to limit=40 and commit. Merge feature-limit into main: both changed the same line, so inspect the conflict rather than hiding it.

```bash
git switch -c feature-limit
printf 'limit=30\n' > policy.txt
git add policy.txt
git commit -m 'Propose feature limit'
git switch main
printf 'limit=40\n' > policy.txt
git add policy.txt
git commit -m 'Revise main limit'
git merge feature-limit
git status
git diff
```

The merge's nonzero/conflict result is expected here. Read the conflicted file; do not bypass it with a destructive cleanup command.

The exercise's agreed new requirement is limit=35. Resolve the file to that value, review it, stage it and finish the merge. Keep the feature branch for graph inspection. Draw both merge parents and explain the business resolution, not merely which conflict button you clicked.

```bash
printf 'limit=35\n' > policy.txt
git add policy.txt
git diff --cached
git commit -m 'Resolve training limit to agreed policy'
git log --graph --oneline --decorate --all
```

## 4. Undo an ordinary bad change safely

After the merge, commit a deliberate limit=999 change. Revert **that new ordinary commit**, not the merge. Confirm the final file is limit=35, both the bad change and its revert remain in history, and the intended worktree is clean.

```bash
printf 'limit=999\n' > policy.txt
git add policy.txt
git commit -m 'Introduce deliberate training mistake'
git log -1 --oneline
git revert --no-edit HEAD
git status --short
git log --graph --oneline --decorate --all
```

Here HEAD means the bad ordinary commit you just created. Inspect it first; do not apply the command blindly to a different history or a merge. Do not rerun these file-writing examples over an existing unrelated attempt without preserving it.

No remote/hosting account/push is required. Do not use hard reset, broad clean or force-push to satisfy a final state.

## Check and evidence

Return to the vault root before the optional read-only check:

```bash
python3 90-tools/check-git-training.py 03-exercises/git/01-local-workflow/work/repo
```

It reads only this marked sandbox and verifies selected branch/history/ignore/file-state properties; it never initializes, commits, stages, fetches or repairs anything. Save a graph, staged/unstaged explanation, conflict reasoning, revert explanation and one review of a change. These manual artifacts, not a green checker alone, complete the lab.

[Hints](hints.md) · [Separate reference reasoning](../../../07-solutions/git-local-workflow/explanation.md)
