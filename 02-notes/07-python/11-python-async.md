# Python 11 — async after synchronous competence

## When to study this

Not on your first Python day. Complete the synchronous language/CLI checkpoint first; read this immediately before the async FastAPI unit. Outcome: distinguish a coroutine, task, awaiting, blocking work, concurrency and cancellation. Practice: api-async after the first synchronous API labs.

```python
import asyncio

async def example():
    await asyncio.sleep(0)
    return 7

# In a standalone script, not inside an already running event loop:
print(asyncio.run(example()))
```

Calling an async function creates a coroutine object; it does not synchronously return its eventual result. Awaiting lets the caller suspend while that operation progresses. A task schedules a coroutine on an event loop. An await is a possible suspension boundary, not a guarantee that every call waits or runs on another thread.

## Resource policies matter more than syntax

async does not automatically make CPU-heavy calculations faster or make a blocking file/database client nonblocking. FastAPI dispatches ordinary def route/dependency functions through its threadpool; a normal helper called directly inside async def is still called directly and can block that event loop.

Bound concurrent operations with a semaphore/worker policy and total input limits. Set application deadlines and understand the underlying client's timeout/cancellation behavior. asyncio.gather does not universally undo effects or clean up every task after one fails; own the tasks you start and cancel/await them deliberately. Do not swallow CancelledError as an ordinary success fallback.

The api-async reference uses asyncio.timeout (Python 3.11+) around owned tasks and awaits cleanup. Cancellation cannot roll back an already committed database write or an external email. Decide idempotency/recovery separately.

## Practice and retrieval

Use controlled events/promises to prove how many operations are in flight. Test a deadline with a never-completing fake, verify its cleanup and distinguish upstream failure (502) from deadline expiry (504). Do not grade correctness by a promised speedup or an exact elapsed duration.

Explain which code runs on the event loop, which can block and where cancellation is observed. Then extend with a retry policy only for explicitly safe/idempotent operations, including a maximum attempt/deadline budget.

Sources: [asyncio tasks](https://docs.python.org/3.14/library/asyncio-task.html), [FastAPI concurrency](https://fastapi.tiangolo.com/async/).
