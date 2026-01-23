import yfinance as yf
import pandas as pd
from fastapi import HTTPException
from typing import Optional, Dict
from app_data.schemas.enums import InvestmentType

class YahooService:
    TYPE_MAPPING = {
        'EQUITY': InvestmentType.ACOES,
        'CRYPTOCURRENCY': InvestmentType.CRIPTO,
        'ETF': InvestmentType.FUNDOS,
        'MUTUALFUND': InvestmentType.FUNDOS
    }

    @staticmethod
    def get_asset_details(ticker: str) -> Optional[Dict]:
        '''
        Busca detalhes completos de um ativo para cadastro.
        '''
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
