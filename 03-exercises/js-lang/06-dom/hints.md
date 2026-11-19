# DOM client — progressive hints

1. Separate pure search/status logic from browser effects. The automated tests intentionally cover only the pure part.
2. Model loading, error and ready explicitly; zero ready records are not a network failure. Use `.includes()` for literal search, not a user-provided RegExp.
3. A latest-request counter prevents stale updates; an AbortController can also stop superseded requests. Build list nodes with textContent. Serve locally and use the fixture modes before consulting reference code.
