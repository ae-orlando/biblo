# Reference: validate, stage, replace

The reference parses explicitly, checks aliases/symlinks and exits before creating a temp file on dry-run. A same-directory temporary file is fully written before `mv` replaces the destination. EXIT cleanup removes only the script's unique file; INT/TERM choose exit statuses explicitly.

This does not establish fsync-based durability, preservation of old destination metadata, or safety against concurrent hostile path replacement. Those require a stronger implementation and threat model. Verification: `python3 90-tools/practice.py check bash-cli --reference`.
