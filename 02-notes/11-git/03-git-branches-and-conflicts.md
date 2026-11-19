# Git 03 — branches, divergence and conflict reasoning

## Outcome

Explain branch pointers and resolve a conflict based on the intended behavior, not by blindly choosing “ours/theirs.” Prerequisite: commits/staging. Practice: the divergence/merge phase of the local workflow exercise.

A branch is a named reference, not a full copied directory. New commits move the current branch. If two branches advance from a common ancestor, their histories diverge. A fast-forward moves a reference when no divergent merge is needed; a true merge can record multiple parents.

```bash
git log --graph --oneline --decorate --all
git branch
git status
```

These observations help determine what state you are actually in. Detached HEAD means HEAD points directly to a commit rather than a branch; preserve valuable new work with a deliberate reference before switching away. Do not assume it disappeared because a branch view changed.

## Resolve meaning, then record the merge

The exercise changes the same policy line differently on main and feature-limit. Git cannot infer the business decision. Read conflict markers and both intended changes, produce the agreed new value, remove markers, review/test, stage the resolution and complete the merge.

Choosing one side can discard meaningful work even when the file becomes syntactically valid. A conflict-free merge can also produce a behavior bug; tests and review remain necessary. A merge commit records ancestry, not a certificate that every feature was retained correctly.

If aborting a merge in a deliberately clean training setup, understand the documented abort operation first; preexisting uncommitted changes can complicate restoration. Do not prescribe hard reset or broad checkout-discard as the universal escape hatch.

## Practice and transfer

Draw the graph before/after the merge and identify both parents. Explain the agreed resolution and show the final behavior. Later compare rebase: it replays changes into new commits and rewrites identities/history relationships. Do not rewrite shared history without a deliberate coordination policy.

Sources: [branching/merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging), [git merge](https://git-scm.com/docs/git-merge), [git rebase](https://git-scm.com/docs/git-rebase).
