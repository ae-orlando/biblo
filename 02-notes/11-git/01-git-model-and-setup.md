# Git 01 — model, identity and repository boundaries

## Outcome

Explain what Git records and choose a safe practice boundary before changing files. Prerequisite: basic terminal/path understanding. Practice: the first phase of the Git local-workflow exercise.

The working tree contains editable files. The index stages a proposed next snapshot. A commit records a tree, parent references and metadata. A branch name points to a commit; HEAD normally names the selected branch. Git stores snapshots/relationships, not a magic backup of every untracked file.

## Inspect before changing anything

```bash
git --version
git rev-parse --show-toplevel
git status --short
```

The last two run in an existing repository; failure outside one is information, not a reason to initialize an arbitrary directory. Know whether you are in a learner repo, a real product repo or the private vault. Do not run destructive repair commands just to get a clean status.

git init creates repository metadata locally; it does not upload content. The exercise lets you deliberately initialize only a new fake-data sandbox. Set an appropriate **repository-local** author identity there; global configuration affects unrelated work and is not needed for this course. Author identity is commit metadata, not remote authentication.

## Boundaries and evidence

A .gitignore controls ordinary untracked-file selection, not OS permissions, encryption or removal of already tracked history. Keep real credentials, local environments, runtime databases and backups out of published history. Lock files and reviewed source/configuration examples can be valuable tracked inputs; do not ignore all JSON or all configuration indiscriminately.

The vault itself has no assumed Git history and has verified snapshots instead. The rebuild never creates/commits a repository on your behalf. Source/notes examples are instructions for your explicit learner actions.

Retrieve: what survives if an untracked file is deleted? What does the index represent before a commit? Why does git config user.email not sign in to a hosting service?

Sources: [Git basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics), [git config](https://git-scm.com/docs/git-config), [git init](https://git-scm.com/docs/git-init).
