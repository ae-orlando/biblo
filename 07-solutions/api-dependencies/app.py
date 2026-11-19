from fastapi import FastAPI
from catalog.domain import Store
from catalog.http import get_store, router


def create_app(store=None):
    app=FastAPI(docs_url=None,redoc_url=None)
    app.state.store=Store() if store is None else store
    app.include_router(router)
    return app
