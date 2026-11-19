# HTTP — progressive hints

1. Keep the server factory separate from listening, so tests choose ports and cleanup explicitly.
2. Count Buffer bytes before decoding. Handle null, arrays and primitive JSON values before reading properties.
3. Use a Map for records and `crypto.randomUUID()` for IDs. Read request chunks with bounded retained memory, handle stream errors/aborts and map expected errors to deliberate statuses. A catch-all `400 invalid JSON` misclassifies other failures.
