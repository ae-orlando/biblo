from dataclasses import dataclass
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, StringConstraints


@dataclass(frozen=True)
class Principal:
    user_id:str
    roles:frozenset[str]=frozenset()


def get_principal():
    # Deliberately unconfigured: a test override is not real authentication.
    raise HTTPException(401,'authentication required',headers={'WWW-Authenticate':'Bearer'})


class Update(BaseModel):
    model_config=ConfigDict(extra='forbid')
    content:Annotated[str,StringConstraints(strict=True,strip_whitespace=True,min_length=1,max_length=1000)]


class Document(BaseModel):
    id:str
    content:str


def create_app():
    documents={'one':{'id':'one','owner_id':'A','content':'A draft'},'two':{'id':'two','owner_id':'B','content':'B draft'}}
    app=FastAPI(docs_url=None,redoc_url=None)
    def accessible(identifier,principal):
        document=documents.get(identifier)
        if document is None or (document['owner_id']!=principal.user_id and 'admin' not in principal.roles):
            raise HTTPException(404,'document not found')
        return document

    @app.get('/documents/{identifier}',response_model=Document)
    def get(identifier:str,principal:Annotated[Principal,Depends(get_principal)]):
        return accessible(identifier,principal)

    @app.put('/documents/{identifier}',response_model=Document)
    def update(identifier:str,body:Update,principal:Annotated[Principal,Depends(get_principal)]):
        document=accessible(identifier,principal)
        document['content']=body.content
        return document

    return app
