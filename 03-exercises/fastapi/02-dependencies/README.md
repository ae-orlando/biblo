# FastAPI lab: isolated state and replaceable dependencies

**ID:** api-dependencies. Prerequisites: first API, Python modules/objects and [[03-fastapi-dependencies]]. Export create_app(store=None) and the actual get_store dependency used by routes.

Each default app has independent in-memory items. POST /items accepts only name, a strict string trimmed to 1..80 characters; create a distinct string ID and return 201 {id,name}. Exact trimmed-name duplicates → 409. GET /items lists records; GET /items/ID returns one or 404. Invalid body → 422. Do not start a listener.

A supplied store exposes all(), create(name) and get(id). app.dependency_overrides[get_store] must genuinely replace the boundary; do not define an unused dummy dependency only for the checker.

```bash
python3 90-tools/practice.py start api-dependencies
python3 90-tools/practice.py check api-dependencies
```

Completion: explain factory/state/dependency lifetimes, show independent apps and a substituted fake, then refactor a meaningful boundary without changing the API. In-memory state/locks are not a multi-worker durable store. See [[web-app-structure]].

[Hints](hints.md) · [Reference explanation](../../../07-solutions/api-dependencies/explanation.md)
