# FastAPI 03 — dependencies, routers and resource ownership

## Outcome

After Python modules/objects and the first API, separate HTTP adaptation from domain work and provide replaceable boundaries. Practice: api-dependencies; architecture examples in [[web-app-structure]].

A dependency is a callable FastAPI resolves as part of request handling. It can provide settings, an authenticated principal or an owned resource. It is not a magical global service locator and does not automatically make its result secure/testable.

Keep app-owned state on a deliberately created app/factory or pass it explicitly. Avoid a shared mutable default store accidentally linking independent app instances. A module-level stateless APIRouter can group routes without owning every app's business state.

The supplied reference has app.py plus a catalog package: domain.py owns store behavior; http.py maps requests/errors; the factory wires state/router. The domain module does not import FastAPI, so its business rules can be reasoned about without a server.

## Lifetimes and cleanup

Distinguish one configuration object per app, one database transaction per operation/request, and resources that require application startup/shutdown. A yield dependency or lifespan context expresses ownership/cleanup for an appropriate lifetime; it does not make a shared connection safe for concurrent requests.

FastAPI normally caches a dependency result within a request; do not infer that it is a global singleton. Use explicit lifetime/configuration and read current documentation when resource behavior matters.

## Practice and retrieval

Complete api-dependencies. Prove independent apps do not share items, duplicates fail deliberately and a dependency override actually replaces the store boundary. Passing a fake in a test does not prove the real database implementation works; that comes later.

Change request: add a case-insensitive name policy or a second repository implementation. Keep HTTP behavior stable and explain which layer owns the changed rule. Do not create unused service/repository layers merely to match a diagram.

Sources: [dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), [yield dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/), [bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/), [lifespan](https://fastapi.tiangolo.com/advanced/events/).
