from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing import Annotated
from store import Repository, DuplicateSKU, MissingItem, InsufficientStock


class NewItem(BaseModel):
    model_config=ConfigDict(extra='forbid')
    sku:Annotated[str,StringConstraints(strict=True,strip_whitespace=True,min_length=1,max_length=40,pattern=r'^[A-Z0-9][A-Z0-9_-]{0,39}$')]
    available:int=Field(strict=True,ge=0,le=1000000)


class Reservation(BaseModel):
    model_config=ConfigDict(extra='forbid')
    quantity:int=Field(strict=True,ge=1,le=1000000)


def create_app(dsn):
    repository=Repository(dsn)
    @asynccontextmanager
    async def lifespan(app):
        # Startup happens once; the request routes below are sync for sync DB I/O.
        await asyncio.to_thread(repository.initialize)
        yield
    app=FastAPI(lifespan=lifespan,docs_url=None,redoc_url=None)
    app.state.repository=repository

    @app.post('/items',status_code=201)
    def create(body:NewItem,request:Request):
        try: return request.app.state.repository.create(body.sku,body.available)
        except DuplicateSKU as error: raise HTTPException(409,'sku already exists') from error

    @app.get('/items/{identifier}')
    def get(identifier:int,request:Request):
        try: return request.app.state.repository.get(identifier)
        except MissingItem as error: raise HTTPException(404,'item not found') from error

    @app.post('/items/{identifier}/reserve')
    def reserve(identifier:int,body:Reservation,request:Request):
        try: return request.app.state.repository.reserve(identifier,body.quantity)
        except MissingItem as error: raise HTTPException(404,'item not found') from error
        except InsufficientStock as error: raise HTTPException(409,'insufficient stock') from error

    return app
