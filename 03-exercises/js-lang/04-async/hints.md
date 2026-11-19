# Async — progressive hints

1. Use a closure-local increasing request number, not the wall clock, to identify the newest call.
2. Check the request number on both success and failure. An old failure should not replace the latest UI state.
3. For bounded mapping, start at most `limit` consumer loops sharing a next-index counter. Store results by original index and attach rejection handling to every started consumer.
