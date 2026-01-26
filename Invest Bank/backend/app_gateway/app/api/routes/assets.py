from fastapi import APIRouter, HTTPException
import yfinance as yf
from app_gateway.services.yfinance_services import YahooService
from app_gateway.services.assets_services import AssetDataService

assets = APIRouter(prefix='/assets', tags=['assets'])

@assets.get('/search/{ticker}')
async def serch_investment_by_ticker(ticker: str):
    '''Busca informações detalhadas de um ativo específico usando o Ticker.'''
    asset_details = YahooService.get_asset_details(ticker)
    if not asset_details:
        raise HTTPException(status_code=404, detail=f'O ticker {ticker} não foi encontrado no sistema do Yahoo Finance.')
    variation = YahooService.get_market_variation(ticker)
    asset_details['variation_24h'] = f"{variation}%"
    return asset_details

@assets.get('/search/{name}')
async def serch_investment_by_name():
    pass

@assets.get('/trending')
async def get_trends():
    pass