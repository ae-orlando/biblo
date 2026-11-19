# Permissions — progressive hints

1. The fake token is training data, not a real credential. Validate the sandbox before attempting repairs.
2. Test every required component for the expected type and reject symbolic links before any chmod.
3. Apply explicit modes to named entries, not recursively to every file. Use `stat` to verify actual modes; “command exited zero” is weaker evidence.
