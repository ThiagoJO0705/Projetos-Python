from fastapi import APIRouter, Depends, Query, HTTPException
from app.api.dependencies import get_session
from app.schemas.schemas import AssetSchema, SearchResponse
from app.schemas.enums import AssetType
from sqlalchemy.orm import Session
from app.models.asset import Asset
from typing import List, Optional
import yfinance as yf

assets = APIRouter(prefix='/assets', tags=['assets'])

@assets.get('/', response_model=List[AssetSchema])
async def get_assets(type: Optional[str] = Query(None, example="AÇÕES ,CRIPTO ou FII"), session: Session = Depends(get_session)):
    '''
    Lista todos os ativos cadastrados no banco de dados
    '''
    assets = session.query(Asset)
    if type is not None:
        type.upper()
        assets = assets.filter(type == Asset.type)
    assets = assets.all()
    return assets


@assets.get('/search', response_model=List[SearchResponse])
async def search_assets(name: str):
    pass
    

@assets.get('/price/{ticker}')
async def get_price():
    pass


@assets.post('/')
async def post_asset():
    pass