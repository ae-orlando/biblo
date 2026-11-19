# Inventory — progressive hints

1. Classify basenames, not full paths; dots in a parent directory are not file extensions.
2. Use associative arrays for counts and byte totals. Avoid arithmetic commands whose false status unexpectedly triggers errexit.
3. Preserve NUL records during traversal and explicitly check the producer status. Keep sorting deterministic. A `head` that closes early can introduce SIGPIPE under pipefail; a reader that consumes the stream is simpler here.
