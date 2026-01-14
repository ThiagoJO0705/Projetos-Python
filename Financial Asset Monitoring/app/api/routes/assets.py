from fastapi import APIRouter, Depends, Query, HTTPException
from app.api.dependencies import get_session
from app.schemas.schemas import AssetSchema, SearchResponse
from app.schemas.enums import AssetType
from sqlalchemy.orm import Session
from app.models.asset import Asset
from typing import List, Optional
import yfinance as yf

assets = APIRouter(prefix='/assets', tags=['assets'])

def map_yahoo_type(yf_item: dict) -> AssetType:
    """
    Converte os metadados do Yahoo Finance para o AssetType
    """
    yf_type = str(yf_item.get('typeDisp', '')).upper()
    symbol = str(yf_item.get('symbol', '')).upper()
    exchange = str(yf_item.get('exchDisp', '')).upper()

    if yf_type in ["CRYPTOCURRENCY", "CURRENCY"] or exchange == "CCC" or "-USD" in symbol:
        return AssetType.CRYPTO

    is_brazilian_market = symbol.endswith(".SA")
    is_fii_pattern = any(symbol.endswith(f"{i}.SA") for i in ["11", "12", "13"])
    
    if yf_type == "ETF" or (is_brazilian_market and is_fii_pattern):
        return AssetType.FII

    if yf_type == "EQUITY":
        return AssetType.STOCKS

    return AssetType.STOCKS


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
    """ Busca no Yahoo Finance por nome e mapeia para o SearchResponse """
    search = yf.Search(name)
    if not search.quotes:
        return []

    search_results = []
    for quote in search.quotes:
        item = SearchResponse(
            ticker=quote.get("symbol"),
            long_name=quote.get("longname"),
            short_name=quote.get("shortname") or quote.get("symbol"),
            stock_exchange=quote.get("exchDisp", "N/A"),
            type=map_yahoo_type(quote)
        )
        search_results.append(item)
    return search_results
    


@assets.get('/price/{ticker}')
async def get_price():
    pass


@assets.post('/')
async def post_asset():
    pass