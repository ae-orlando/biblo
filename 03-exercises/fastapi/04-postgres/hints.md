# Persistent reservations — progressive hints

1. Never share one mutable connection across arbitrary concurrent request handlers. Store configuration, acquire/close owned operation resources.
2. Request validation and SQL constraints protect different boundaries. A read/check/subtract sequence can race.
3. A conditional UPDATE with RETURNING can enforce the one-row stock invariant atomically. Distinguish missing from insufficient stock and keep errors inside the intended transaction boundary. No DELETE route is part of this exercise.
