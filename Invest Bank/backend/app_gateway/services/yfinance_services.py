import yfinance as yf
import numpy as np
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
        ticker_upper = ticker.upper()
        asset = yf.Ticker(ticker_upper)
        try:
            fast = asset.fast_info
            price = fast.get('last_price')
            if price is None or np.isnan(price):
                hist = asset.history(period="1d")
                if hist.empty:
                    return None
                price = hist['Close'].iloc[-1]
            try:
                info = asset.info
                name = info.get('longName') or info.get('shortName') or ticker_upper
                yahoo_type = info.get('quoteType', 'EQUITY')
            except Exception:
                name = ticker_upper
                yahoo_type = 'EQUITY'

            mapped_type = YahooService.TYPE_MAPPING.get(yahoo_type, InvestmentType.STOCKS)

            return {
                'ticker': ticker_upper,
                'name': name,
                'type': mapped_type,
                'current_price': round(float(price), 2)
            }
        except Exception:
            return None

    @staticmethod
    def get_current_price(ticker: str) -> float:
        '''Busca o preço atual deum um ativo'''
        try:
            asset = yf.Ticker(ticker)
            price = asset.fast_info['last_price']
            return round(float(price), 2) if not np.isnan(price) else 0.0
        except Exception:
            return 0.0

    @staticmethod
    def get_historical_data(ticker: str, period: str = '1y') -> pd.DataFrame:
        '''Retorna um DataFrame do Pandas com o histórico de preços.'''
        try:
            asset = yf.Ticker(ticker.upper())
            df = asset.history(period=period)
            if df.empty:
                raise ValueError('Ticker sem histórico.')
            return df
        except Exception:
            return pd.DataFrame()

    @staticmethod
    def get_market_variation(ticker: str) -> float:
        '''Calcula a variação percentual do ativo nas últimas 24h.'''
        try:
            asset = yf.Ticker(ticker.upper())
            history = asset.history(period='2d')
            if len(history) < 2:
                return 0.0
            price_close = history['Close'].iloc[-1]
            price_prev = history['Close'].iloc[-2]
            variation = ((price_close - price_prev) / price_prev) * 100
            return round(variation, 2)
        except Exception:
            return 0.0