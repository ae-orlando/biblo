# Web application structures — appropriate, not universally ideal

## Outcome

Choose a structure that makes ownership, dependencies, testing and delivery understandable. There is no single ideal tree for every web app. Begin with the smallest structure that keeps important boundaries clear, then refactor in response to real complexity.

| Situation | Sensible starting point | Reason to grow |
| --- | --- | --- |
| One static page | HTML, one stylesheet, deliberate public assets | Repeated components/behavior/assets become hard to navigate |
| Small Python CLI | Entry point, reusable module, tests, dependency metadata when needed | Several responsibilities or reusable package entry points |
| First FastAPI app | One factory module and request tests | Features/domain work/resources become difficult to isolate |
| Small multi-feature API | Factory plus feature packages and explicit persistence/configuration boundaries | Cross-feature workflows, ownership and scaling constraints justify more separation |
| Fullstack product | Explicit frontend/backend/public/deployment boundaries | Independent teams/releases or a genuine service boundary, not fashion |

## Read a real example before copying a template

The api-dependencies reference actually contains:

```text
07-solutions/api-dependencies/
  app.py                 # composition: create app, attach state, include router
  catalog/
    __init__.py
    domain.py            # store behavior, no FastAPI import
    http.py              # request/response schemas, dependency, HTTP adaptation
```

See `07-solutions/api-dependencies/app.py:1`, `catalog/domain.py:1` and `catalog/http.py:1` under that directory. The api-postgres reference deliberately uses only app.py + store.py for another small scope. Neither tree is a universal production template; both are runnable examples whose behavior is checked.

## Core principles

- Put files together when they change for the same reason; separate boundaries that need different ownership/testing/lifetimes.
- Keep imports directed: domain rules do not import the CLI/router that calls them.
- Keep reusable imports free of environment-dependent startup/network/filesystem effects.
- Separate source, tests, deliberate public assets, configuration examples and generated/runtime data.
- Never serve the repository/vault root just because it contains a frontend index.html.
- Do not add empty controllers/services/repositories/factories merely to imitate enterprise terminology.

## Next decisions and practice

Read [[01-fastapi-project-layouts]] for growth stages, [[02-fullstack-repository-layouts]] for frontend/backend choices and [[03-boundaries-and-refactoring]] for a concrete refactor. Learn structure after [[08-python-modules]], not before your first function.

Explain where a new validation rule, query, UI state and deployment setting would go—and what should remain unchanged. A pretty directory tree without a working test/entry point is not architecture evidence.

Sources: [FastAPI bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/), [PyPA src versus flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
