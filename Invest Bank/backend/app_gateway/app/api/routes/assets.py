from fastapi import APIRouter, HTTPException
import yfinance as yf
from app_gateway.services.yfinance_services import YahooService
from app_gateway.services.assets_services import AssetDataService

assets = APIRouter(prefix='/assets', tags=['assets'])

@assets.get('/search/ticker/{ticker}')
async def serch_investment_by_ticker(ticker: str):
    '''Busca informações detalhadas de um ativo específico usando o Ticker.'''
    asset_details = YahooService.get_asset_details(ticker)
    if not asset_details:
        raise HTTPException(status_code=404, detail=f'O ticker {ticker} não foi encontrado no sistema do Yahoo Finance.')
    variation = YahooService.get_market_variation(ticker)
    asset_details['variation_24h'] = f"{variation}%"
    return asset_details

@assets.get('/search/name/{name}')
async def serch_investment_by_name(name: str):
    '''Busca Tickers baseados no nome da empresa ou ativo.'''
    try:
        search = yf.Search(name, max_results=5)
        results = []
        for quote in search.quotes:
            results.append({
                'ticker': quote.get('symbol'),
                'name': quote.get('shortname') or quote.get('longname'),
                'exchange': quote.get('exchange'),
                'type': quote.get('quoteType')
            })
        if not results:
            raise HTTPException(status_code=404, detail="Nenhum ativo encontrado com este nome.")
        return results
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao realizar busca por nome no Yahoo Finance.")

@assets.get('/trending')
async def get_trends():
    pass