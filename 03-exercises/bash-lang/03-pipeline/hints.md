# Log stream — progressive hints

1. Printing a summary incrementally conflicts with the requirement to reject a bad final line without partial output.
2. Track counts and an error flag; emit only at end when all records were valid.
3. awk can validate field structure, report the failing line on stderr, and return nonzero from END. The shell should preserve that status rather than suppress it with `|| true`.
