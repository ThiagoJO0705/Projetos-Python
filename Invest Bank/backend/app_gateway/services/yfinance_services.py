import yfinance as yf
import pandas as pd
from fastapi import HTTPException
from typing import Optional, Dict
from app_data.schemas.enums import InvestmentType

class YahooService:
    TYPE_MAPPING = {
        'EQUITY': InvestmentType.STOCKS,
        'CRYPTOCURRENCY': InvestmentType.CRYPTO,
        'ETF': InvestmentType.FUNDS,
        'MUTUALFUND': InvestmentType.FUNDS
    }

    @staticmethod
    def get_asset_details(ticker: str) -> Optional[Dict]:
        '''Busca detalhes completos de um ativo para cadastro.'''
        try:
            asset = yf.Ticker(ticker)
            info = asset.info
            if not info or 'symbol' not in info:
                return None
            yahoo_type = info.get('quoteType', 'EQUITY')
            mapped_type = YahooService.TYPE_MAPPING.get(yahoo_type, InvestmentType.ACOES)
            return {
                'ticker': ticker.upper(),
                'name': info.get('longName') or info.get('shortName') or ticker,
                'type': mapped_type,
                'current_price': info.get('regularMarketPrice') or info.get('currentPrice') or 0.0
            }
        except Exception:
            return None

    @staticmethod
    def get_current_price(ticker: str) -> float:
        '''Busca o preço atual deum um ativo'''
        try:
            asset = yf.Ticker(ticker)
            return asset.fast_info['last_price']
        except Exception:
            return 0.0

    @staticmethod
    def get_historical_data(ticker: str, period: str = '1y') -> pd.DataFrame:
        '''Retorna um DataFrame do Pandas com o histórico de preços.'''
        try:
            asset = yf.Ticker(ticker)
            df = asset.history(period=period)
            if df.empty:
                raise ValueError('Nenhum dado histórico encontrado.')
            return df
        except Exception:
            raise HTTPException(status_code=400, detail=f'Erro ao buscar histórico do ativo no YahooFinance')

    @staticmethod
    def get_market_variation(ticker: str) -> float:
        '''Calcula a variação percentual do ativo nas últimas 24h.'''
        try:
            asset = yf.Ticker(ticker)
            history = asset.history(period='2d')
            if len(history) < 2:
                return 0.0
            price_close = history['Close'].iloc[-1]
            price_prev = history['Close'].iloc[-2]
            variation = ((price_close - price_prev) / price_prev) * 100
            return round(variation, 2)
        except Exception:
            return 0.0