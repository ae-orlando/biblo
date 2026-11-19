from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field


class QuoteInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    quantity:int=Field(strict=True,ge=1,le=1000000)
    unit_price_cents:int=Field(strict=True,ge=0,le=1000000)


class QuoteOutput(BaseModel):
    quantity:int
    unit_price_cents:int
    total_cents:int


def create_app():
    app=FastAPI(docs_url=None,redoc_url=None)

    @app.get('/health')
    def health(): return {'status':'ok'}

    @app.post('/quotes',response_model=QuoteOutput)
    def quote(body:QuoteInput):
        return {'quantity':body.quantity,'unit_price_cents':body.unit_price_cents,'total_cents':body.quantity*body.unit_price_cents}

    return app
