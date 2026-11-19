# FastAPI project layouts — grow from working boundaries

## Small first app

For api-contract, one app.py with a factory and tests is appropriate. Splitting three lines into ten empty modules does not improve engineering. Keep the factory importable without starting a server and avoid mutable global application state.

## A feature package when complexity appears

The api-dependencies reference demonstrates a real catalog package: HTTP adaptation is separate from domain/store behavior. The entry factory wires dependencies. You can test domain rules without HTTP and request contracts through the app factory.

When a larger application genuinely needs separation, this is an **illustrative design**, not an already generated/runnable project:

```text
backend/
  pyproject.toml
  dependency-lock-file
  README.md
  .env.example
  src/
    library_api/
      __init__.py
      main.py                 # app factory and composition
      settings.py             # validated settings, no real secrets in source
      database.py             # connection/pool lifecycle
      catalog/
        __init__.py
        router.py             # HTTP concerns
        schemas.py            # external representations
        service.py            # only if a nontrivial use case justifies it
        repository.py         # persistence adapter, if useful
  migrations/                 # selected tool/version policy, not boot-time guessing
  tests/
    unit/
    integration/
```

Choose your actual packaging/dependency/migration tools, make the entry point work, and verify commands before documenting them. A src layout is useful when you want tests/imports to use the installed package; it introduces installation/configuration obligations that a first one-file lab does not need.

## Avoid common mistakes

- A Pydantic request schema, database row/model and domain concept may have different fields and trust. Do not blindly expose a persistence object containing private fields.
- A service layer should own meaningful workflows/invariants, not forward every call unchanged for appearance.
- A repository should not secretly commit half a workflow that must be atomic across several operations. Define a transaction/unit-of-work boundary explicitly.
- A dependency's request lifetime does not automatically guarantee one OS thread or make a connection safe to share concurrently.
- Migration application belongs to a reviewed delivery policy; CREATE TABLE IF NOT EXISTS at every startup is only the lab's bootstrap convenience.

## Exercise

Choose one completed API lab and identify its change hotspots. Extract one real boundary while keeping behavior/tests stable. Explain import direction, state lifetime and transaction ownership before adding another layer. Use [[03-boundaries-and-refactoring]].

Sources: [FastAPI packages/routers](https://fastapi.tiangolo.com/tutorial/bigger-applications/), [application lifespan](https://fastapi.tiangolo.com/advanced/events/), [PyPA layouts](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
