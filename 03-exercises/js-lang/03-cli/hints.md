# CLI — progressive hints

1. Decide which errors are usage errors before touching the filesystem.
2. ESM allows top-level await. Read as UTF-8, parse JSON, then validate its structure before totaling.
3. Set `process.exitCode` and write errors to stderr. Only print the final JSON after all validation has succeeded; partial success output breaks callers.
