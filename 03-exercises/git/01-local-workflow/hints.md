# Git workflow — progressive hints

1. Identify which comparison you want: working tree versus index, or index versus HEAD. Staging records the current version, not every later edit automatically.
2. Branches must genuinely diverge from a common ancestor to produce this conflict; inspect the graph instead of adding arbitrary extra commits.
3. A resolved merge can intentionally contain a new agreed value. A later revert should target the deliberately bad ordinary commit, preserving the merge history. Consult command help before changing state; the read-only checker does not repair it for you.
