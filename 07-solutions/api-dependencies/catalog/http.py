from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict, StringConstraints
from .domain import DuplicateName, Store

router=APIRouter(prefix='/items')


class NewItem(BaseModel):
    model_config=ConfigDict(extra='forbid')
    name:Annotated[str,StringConstraints(strict=True,strip_whitespace=True,min_length=1,max_length=80)]


class Item(BaseModel):
    id:str
    name:str


def get_store(request:Request): return request.app.state.store


@router.get('',response_model=list[Item])
def list_items(store:Annotated[Store,Depends(get_store)]): return store.all()


@router.post('',response_model=Item,status_code=201)
def create_item(body:NewItem,store:Annotated[Store,Depends(get_store)]):
    try: return store.create(body.name)
    except DuplicateName as error: raise HTTPException(409,'name already exists') from error


@router.get('/{identifier}',response_model=Item)
def get_item(identifier:str,store:Annotated[Store,Depends(get_store)]):
    try: return store.get(identifier)
    except KeyError as error: raise HTTPException(404,'item not found') from error
