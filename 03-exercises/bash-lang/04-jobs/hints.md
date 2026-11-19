# Worker lifecycle — progressive hints

1. Save each `$!` immediately. “Wait for everything” alone does not tell you which job failed.
2. Use EXIT cleanup and separate signal handlers that select exit statuses. Save `$?` before cleanup commands overwrite it.
3. Cleanup only your recorded children, then `wait` for each, tolerating expected nonzero terminated statuses. Remove only your unique empty directory. Quoting alone does not make a broad delete safe.
