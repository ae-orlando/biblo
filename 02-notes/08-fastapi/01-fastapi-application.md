# FastAPI 01 — application, server and request path

## Outcome

After Python's checkpoint and HTTP basics, explain the difference between your function, FastAPI, ASGI and the server. Practice: api-contract. Do not begin by copying a full project generator.

FastAPI registers route handlers and coordinates request parsing, dependencies and responses. An ASGI server such as Uvicorn accepts connections and invokes the app through the ASGI interface. A decorator registers a path operation; it is not the network listener itself.

```python
from fastapi import FastAPI

def create_app():
    app = FastAPI()
    @app.get("/health")
    def health():
        return {"status": "ok"}
    return app
```

This is an explanatory factory example; the api-contract lab has additional requirements. An app factory lets each test create isolated state/configuration. Keep import-time code free of server startup, network calls and production configuration reads.

## Run versus test

The bundled check imports your factory and uses TestClient in a context manager. That exercises the app's lifespan and HTTP contract without opening a listening port. A real server is a different boundary; bind a training app only to loopback.

For a supplied reference with a no-argument factory, the local Uvicorn command is:

```bash
.tools/fastapi-env/bin/python -m uvicorn --app-dir 07-solutions/api-contract app:create_app --factory --host 127.0.0.1 --port 8000
```

Use Ctrl-C to stop it; choose another port if occupied. This command runs the reference for inspection, not learner completion. Do not reuse it for api-postgres without explicitly supplying its required configuration; its checks inject a private practice DSN.

## Practice and retrieval

Implement the lab's health and quote routes. Explain method/path selection, request parsing, route call and JSON response. Inspect OpenAPI and status codes, including 404 versus 405. A JSON response alone is not proof of a correct business result or safe deployment.

Sources: [first steps](https://fastapi.tiangolo.com/tutorial/first-steps/), [manual serving](https://fastapi.tiangolo.com/deployment/manually/), [ASGI](https://asgi.readthedocs.io/en/latest/specs/main.html).
