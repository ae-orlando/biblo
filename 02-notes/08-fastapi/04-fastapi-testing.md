# FastAPI 04 — test the contract and its real boundaries

## Outcome

Distinguish a request contract test, domain test, database integration test and deployed-system test. Prerequisites: Python tests and the first two API labs. Apply to all FastAPI labs.

TestClient invokes an ASGI application in-process. Use its context manager so startup/shutdown runs. Each test should own independent application state and a disposable dataset. The curriculum runs these checks with unittest; pytest is optional rather than another immediate prerequisite.

Assert status, relevant headers/body, unchanged state after rejection and meaningful negative cases. A passing dependency override proves the app can use that substituted boundary; it does not prove the real dependency's transaction behavior. Use api-postgres for actual database/concurrency evidence.

## Resource/identity isolation

- Factories keep state/configuration explicit and prevent tests sharing accidental globals.
- A fresh private database prevents fixtures from modifying real data.
- Auth tests can inject a trusted principal to isolate **authorization**. That is not proof that a real bearer token or session is verified correctly.
- Explicit lifespan cleanup avoids abandoned resources. Test clients do not exercise DNS, reverse proxies or TLS.

The installed Starlette/TestClient version prefers httpx2; some upstream examples still describe httpx. The local runtime pins both for compatibility/reference and records resolved versions. Use the verified installer rather than mixing arbitrary tutorial dependency versions; see [[python-fastapi-expansion-status]].

## Deliberate regressions

Remove a strict field, use global app state, subtract stock without checking availability or skip ownership enforcement in a disposable copy. The corresponding test must fail. If not, add the missing discriminating case. Do not hide deprecations/errors as a way to claim a clean suite.

Completion: explain one failure the tests establish, one they do not establish, and meet a changed requirement without copying a full solution. Continue into async or SQL only after their prerequisites are understood.

Sources: [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/), [dependency overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/), [lifespan tests](https://fastapi.tiangolo.com/advanced/testing-events/).
