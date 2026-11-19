# FastAPI 05 — async I/O, limits and failure cleanup

## Outcome and prerequisites

Read [[11-python-async]] after the synchronous API labs. Outcome: handle slow/failing dependencies without unbounded work or abandoned tasks. Practice: api-async.

Use async def when the work you call has a genuinely awaitable interface; ordinary blocking calls do not become nonblocking because their caller is async. FastAPI runs ordinary def route/dependency functions in its worker threadpool, but does not automatically offload every normal helper called inside async code. A finite threadpool is still a resource limit.

## Bound inputs, work and waiting

Specify maximum request size/count, maximum in-flight operations and a deadline. These are different limits. A semaphore caps work that passed the gate; a huge list of created tasks can still consume memory, so cap batch input too. The lab caps codes at ten and in-flight workers at two by default.

Cancellation is a request to stop cooperative work. The underlying operation must support it, and an already committed effect is not rolled back. Own tasks you start, cancel remaining work on failure/deadline and await cleanup. Do not return a success result after swallowing cancellation.

The bundled helper surrounds owned tasks with asyncio.timeout. It does not implement arbitrary retries. Retries require a bounded budget and an explicit transient/idempotency policy; retrying every failure can multiply load or duplicate effects.

## Test the schedule, not a speed promise

Use events to hold workers at a known point and count in-flight work. Assert all workers leave after a timeout. A bounded test timeout prevents a hang; asserting that concurrent code is exactly N times faster is not a correctness check.

At the HTTP boundary, the exercise maps expected upstream failure to 502 and a deadline to 504, without disclosing private upstream messages. Those are the chosen contracts, not an instruction to turn every programming defect into a 502.

Completion: explain the task lifecycle and cancellation boundary, pass api-async, introduce a missing-bound/cleanup defect in a disposable copy, then add a new safe requirement with a regression case. Real network clients additionally need connection/read/write/pool limits and application-lifespan ownership.

Sources: [FastAPI async](https://fastapi.tiangolo.com/async/), [asyncio tasks](https://docs.python.org/3.14/library/asyncio-task.html).
