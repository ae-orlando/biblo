from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field
from pydantic import StringConstraints
from typing import Annotated
from async_tools import GatewayError, total_prices


class Codes(BaseModel):
    model_config=ConfigDict(extra='forbid')
    codes:list[Annotated[str,StringConstraints(strict=True,strip_whitespace=True,min_length=1,max_length=40)]]=Field(min_length=1,max_length=10)


async def fixture_price(code):
    try: return {'A':100,'B':250,'FREE':0}[code]
    except KeyError as error: raise GatewayError('upstream has no price') from error


def create_app(fetcher=None,timeout=0.2,limit=2):
    app=FastAPI(docs_url=None,redoc_url=None)
    app.state.fetcher=fixture_price if fetcher is None else fetcher

    @app.post('/totals')
    async def totals(body:Codes,request:Request):
        try:
            amount=await total_prices(body.codes,request.app.state.fetcher,limit,timeout)
            return {'count':len(body.codes),'total_cents':amount}
        except TimeoutError as error: raise HTTPException(504,'upstream deadline exceeded') from error
        except GatewayError as error: raise HTTPException(502,'upstream failed') from error

    return app
