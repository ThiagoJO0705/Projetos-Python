import yfinance as yf
import numpy as np
import pandas as pd
from fastapi import HTTPException
from typing import Optional, Dict
from app_data.schemas.enums import InvestmentType
from datetime import datetime, timedelta

class YahooService:
    TYPE_MAPPING = {
        'EQUITY': InvestmentType.STOCKS,
        'CRYPTOCURRENCY': InvestmentType.CRYPTO,
        'ETF': InvestmentType.FUNDS,
        'MUTUALFUND': InvestmentType.FUNDS
    }

    @staticmethod
    def get_usd_brl_rate() -> float:
        '''Busca a cotação atual do Dólar para Real (USDBRL=X).'''
        try:
            usd_ticker = yf.Ticker('USDBRL=X')
            rate = usd_ticker.fast_info['last_price']
            return float(rate)
        except Exception:
            return 5.0

    @staticmethod
    def get_asset_details(ticker: str) -> Optional[Dict]:
        '''Busca detalhes completos de um ativo para cadastro.'''
        ticker_upper = ticker.upper()
        asset = yf.Ticker(ticker_upper)
        try:
            price = None
            try:
                fast = asset.fast_info
                price = fast.get('last_price') or fast.get('lastPrice')
            except:
                pass
            if price is None or np.isnan(price) or price == 0:
                hist = asset.history(period='1d')
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                else:
                    return None 
            name = ticker_upper
            yahoo_type = None
            currency = 'BRL'
            try:
                info = asset.info
                if info and isinstance(info, dict):
                    name = info.get('longName') or info.get('shortName') or ticker_upper
                    yahoo_type = info.get('quoteType', 'EQUITY')
                    currency = info.get('currency', 'BRL')
            except Exception:
                pass
            if ticker_upper.endswith('11.SA'):
                mapped_type = InvestmentType.FUNDS
            elif yahoo_type in ['ETF', 'MUTUALFUND']:
                mapped_type = InvestmentType.FUNDS
            elif yahoo_type == 'CRYPTOCURRENCY' or ticker_upper.endswith('-USD'):
                mapped_type = InvestmentType.CRYPTO
            else:
                mapped_type = YahooService.TYPE_MAPPING.get(yahoo_type, InvestmentType.STOCKS)
            return {
                'ticker': ticker_upper,
                'name': name,
                'type': mapped_type,
                'current_price': round(float(price), 2),
                'currency': currency
            }
        except Exception as e:
            print(f"Erro ao buscar {ticker_upper}: {e}")
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
        
    @staticmethod
    def get_price_on_date(ticker: str, purchase_date: str) -> Optional[Dict[str, float]]:
        '''Busca a mínima e a máxima de um ativo em uma data específica.'''
        try:
            start_dt = datetime.strptime(purchase_date, '%Y-%m-%d')
            end_dt = start_dt + timedelta(days=1)
            asset = yf.Ticker(ticker.upper())
            history = asset.history(start=start_dt.strftime('%Y-%m-%d'), end=end_dt.strftime('%Y-%m-%d'))
            if history.empty:
                return None
            return {
                'day_low': float(history['Low'].iloc[0]),
                'day_high': float(history['High'].iloc[0])
            }
        except Exception:
            return None

    @staticmethod
    def get_usd_brl_rate_on_date(purchase_date: str) -> float:
        '''Busca a cotação do dólar (USDBRL=X) em uma data específica do passado.'''
        try:
            start_dt = datetime.strptime(purchase_date, "%Y-%m-%d")
            end_dt = start_dt + timedelta(days=1)
            usd_ticker = yf.Ticker("USDBRL=X")
            history = usd_ticker.history(start=start_dt.strftime('%Y-%m-%d'), end=end_dt.strftime('%Y-%m-%d'))
            if history.empty:
                return YahooService.get_usd_brl_rate() 
            return float(history['Close'].iloc[0])
        except Exception:
            return 5.0