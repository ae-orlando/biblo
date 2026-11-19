# Reference reasoning: local workflow, not fabricated execution

The intended staging observation is HEAD=10, index=20, working file=25. Committing the later intended snapshot requires deliberately staging it; a normal commit would otherwise use the older staged value.

The branch exercise has a shared ancestor, a feature-side 30 change and a main-side 40 change. The agreed resolution 35 is a business decision; the merge records both parents but does not certify that the decision was wise. A subsequent 999 commit and its revert retain an audit trail while restoring 35.

The final state includes main and feature-limit, a real merge ancestor, a clean intended worktree, policy.txt containing limit=35 and a fake .env ignored/not tracked. A plausible schematic is:

```text
A--B--C--D--M--E--R  main
       \--F--/
```

Letters are explanatory placeholders, not actual commit hashes or claims that these Git operations were executed. The author did not create a repo or commits. You must produce your own graph, diffs and reasoning. Selected artifact checks are not a competence certificate or real team review.
