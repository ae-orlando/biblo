/# Git learning path — preserve, inspect and collaborate

Learn Git as a model of changes/history, not a list of rescue commands. Use it after you have a small working program worth preserving; it need not compete with your first Python syntax lesson.

## Sequence

| Unit | Read | Evidence |
| --- | --- | --- |
| Model and scope | [[01-git-model-and-setup]] | Explain working tree/index/commit and identify the actual repo root |
| Deliberate changes | [[02-git-staging-and-commits]] | Show distinct staged/unstaged versions and review the exact next snapshot |
| Histories | [[03-git-branches-and-conflicts]] | Create diverging work, resolve a real conflict and explain the merge parents |
| Collaboration | [[04-git-remotes-and-review]] | Explain fetch/integration/push and review a change; no remote account required |
| Recovery/security | [[05-git-recovery-and-secrets]] | Revert intentionally, preserve work and keep fake/real secret policies distinct |

The [local workflow exercise](../../03-exercises/git/01-local-workflow/README.md) combines these skills. It contains commands **you deliberately run in a disposable learner repository**, not operations the vault rebuild executes. No repository, commit, remote, global identity setting or publication is created automatically.

The optional checker reads only an explicitly marked repository under 03-exercises/git/. It verifies selected final-state properties; it does not certify your explanation, conflict reasoning, review quality or a real collaboration experience.

## Completion

Preserve reviewed diffs, explain the graph and staged/unstaged distinction, demonstrate a deliberate conflict and safe revert, and review another change against its contract/tests. A clean status or arbitrary commit count alone is not competence.

Sources: [Git documentation](https://git-scm.com/docs), [Pro Git](https://git-scm.com/book/en/v2). Existing [[15-git-and-collaboration]] remains a compact reference linking to this expanded course.
