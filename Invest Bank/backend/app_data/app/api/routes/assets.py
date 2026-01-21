from fastapi import APIRouter, HTTPException, Depends, status
from app_data.schemas.schemas import AssetBase, AssetResponse
from app_data.app.dbconfig import get_session
from sqlalchemy.orm import Session
from app_data.models.asset import Asset
import yfinance as yf

assets = APIRouter(prefix='/assets', tags=['assets'])

@assets.post('/', response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(asset: AssetBase, session: Session = Depends(get_session)):
    '''
    Registra um novo ativo no banco de dados
    '''
    existing = session.query(Asset).filter(Asset.ticker == asset.ticker.upper()).first()
    if existing:
        raise HTTPException(status_code=400, detail='Este ativo já está cadastrado no banco de dados.')
    new_asset = Asset(
        ticker=asset.ticker.upper(),
        name=asset.name,
        type=asset.type,
        current_price=asset.current_price
    )
    try:
        session.add(new_asset)
        session.commit()
        session.refresh(new_asset)
        return new_asset
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail='Ocorreu um erro ao tentar salvar no banco de dados. ')

@assets.get('/')
async def get_assets():
    pass

@assets.get('/{ticker}')
async def get_asset_by_ticker():
    pass

@assets.patch('/{id}')
async def get_asset_by_ticker():
    pass