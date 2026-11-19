# Async API — progressive hints

1. Limit batch size and in-flight work separately. A semaphore is not a total request-size limit.
2. Own references to tasks so you can cancel and await them when another task fails or a deadline expires.
3. Keep expected gateway failures distinct from deadline expiry; map them at the HTTP boundary without returning private exception messages. Cancellation is not rollback of external effects.
