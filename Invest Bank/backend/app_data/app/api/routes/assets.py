from fastapi import APIRouter, HTTPException, Depends, status
from app_data.schemas.schemas import AssetBase, AssetResponse, AssetUpdate
from app_data.app.dbconfig import get_session
from sqlalchemy.orm import Session
from app_data.models.asset import Asset
from typing import List
import yfinance as yf
import uuid

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
        current_price=asset.current_price,
        currency=asset.currency
    )
    try:
        session.add(new_asset)
        session.commit()
        session.refresh(new_asset)
        return new_asset
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail='Ocorreu um erro ao tentar salvar no banco de dados. ')

@assets.get('/', response_model=List[AssetResponse])
async def get_assets(session: Session = Depends(get_session)):
    '''
    Busca todos os ativos cadastrados no banco de dados
    '''
    assets = session.query(Asset).all()
    return assets
    

@assets.get('/{ticker}', response_model=AssetResponse)
async def get_asset_by_ticker(ticker: str, session: Session = Depends(get_session)):
    '''
    Busca um ativo cadastrado no banco pelo Ticker informado
    '''
    existing_asset = session.query(Asset).filter(ticker.upper() == Asset.ticker).first()
    if not existing_asset:
        raise HTTPException(status_code=404, detail='Ativo não encontrado. Verifique o Ticker informado.')
    return existing_asset

@assets.patch('/{asset_id}', response_model=AssetResponse)
async def update_asset(asset_id: uuid.UUID, asset_update: AssetUpdate, session: Session = Depends(get_session)):
    '''
    Atualiza dados de um Ativo
    '''
    asset = session.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail='Ativo não encontrado.')
    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asset, key, value)
    try:
        session.commit()
        session.refresh(asset)
        return asset
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f'Ocorreu um erro ao atualizar o ativo')