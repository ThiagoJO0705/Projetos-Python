from fastapi import APIRouter, Depends, Query, HTTPException
from app.api.dependencies import get_session, verify_token
from app.schemas.schemas import AssetSchema, SearchResponse, AssetPrice, TickerSchema
from app.schemas.enums import AssetType
from sqlalchemy.orm import Session
from app.models.user import User
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
    type = type.upper()
    if type is not None:
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
    


@assets.get('/price/{ticker}', response_model=AssetPrice)
async def get_price(ticker: str):
    """ Retorna o preço atual de um ativo específico """
    try:
        tck = yf.Ticker(ticker)
        price = tck.fast_info.last_price
        currency = tck.fast_info.currency
        asset_price = AssetPrice(
            ticker=ticker.upper(),
            price=round(price, 2),
            currency=currency)
        return asset_price
    except Exception:
        raise HTTPException(status_code=404, detail="Não foi possível obter o preço deste ticker")


@assets.post('/')
async def post_asset(ticker_schema: TickerSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    existing = session.query(Asset).filter(Asset.ticker == ticker_schema.ticker).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ativo já cadastrado")
    tck = yf.Ticker(ticker_schema.ticker)
    try:
        info = tck.info
        if not info or 'symbol' not in info:
            raise HTTPException(status_code=400, detail="Ticker inválido ou não encontrado no Yahoo Finance.")
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao validar Ticker. Verifique a conexão ou o código digitado.")
    new_asset = Asset(
        name=info.get('longName') or info.get('shortName'),
        ticker=ticker_schema.ticker.upper(),
        type=map_yahoo_type(info)
    )
    session.add(new_asset)
    session.commit()
    session.refresh(new_asset)
    return new_asset