import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app_data.schemas.enums import InvestorProfile, InvestmentType

class AnalysisService:
    PROJECTION_RATES = {
        InvestorProfile.CONSERVATIVE: 0.08,
        InvestorProfile.MODERATE: 0.12,
        InvestorProfile.BOLD: 0.18,
        InvestorProfile.UNDEFINED: 0.00
    }

    @staticmethod
    def _extract_ticker(asset_dict: Dict) -> str:
        '''Extrai o ticker do objeto asset.'''
        if asset_dict and 'ticker' in asset_dict:
            return asset_dict['ticker']
        return 'N/A'

    @staticmethod
    def _extract_price(asset_dict: Dict) -> float:
        '''Extrai o preço atual do objeto asset.'''
        if asset_dict and 'current_price' in asset_dict:
            return float(asset_dict['current_price'])
        return 0.0

    @staticmethod
    def _extract_type(asset_dict: Dict) -> str:
        '''Extrai o tipo de investimento do objeto asset.'''
        if asset_dict and 'type' in asset_dict:
            return asset_dict['type']
        return 'OTHER'

    @staticmethod
    def get_portfolio_analysis(investments: List[Dict[str, Any]], profile: InvestorProfile) -> Dict[str, Any]:
        '''Gera uma análise da carteira do cliente.'''
        if not investments:
            return {
                'total_invested': 0.0,
                'current_portfolio_value': 0.0,
                'total_profit_loss': 0.0,
                'global_yield_pct': 0.0,
                'portfolio_items': []
            }

        df = pd.DataFrame(investments)
        df['ticker'] = df['asset'].apply(AnalysisService._extract_ticker)
        df['current_market_price'] = df['asset'].apply(AnalysisService._extract_price)
        df['investment_type'] = df['asset'].apply(AnalysisService._extract_type)
        df['quantity'] = df['quantity'].astype(float)
        df['purchase_price'] = df['purchase_price'].astype(float)
        df['total_purchase_value'] = df['quantity'] * df['purchase_price']
        profile_rate = AnalysisService.PROJECTION_RATES.get(profile, 0.0)

        def calculate_current_value(row):
            '''Calcula valor atual do ativo para projeção'''
            if row['investment_type'] == InvestmentType.RENDA_FIXA:
                return row['total_purchase_value'] * (1 + profile_rate)
            return row['quantity'] * row['current_market_price']

        df['current_value'] = df.apply(calculate_current_value, axis=1)
        df['profit_loss'] = df['current_value'] - df['total_purchase_value']
        total_invested = np.sum(df['total_purchase_value'])
        current_portfolio_value = np.sum(df['current_value'])
        total_profit_loss = current_portfolio_value - total_invested
        global_yield_pct = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0.0

        return {
            'analyzed_profile': profile,
            'applied_projection_rate': f'{profile_rate * 100}%',
            'total_invested': round(float(total_invested), 2),
            'current_portfolio_value': round(float(current_portfolio_value), 2),
            'total_profit_loss': round(float(total_profit_loss), 2),
            'global_yield_pct': round(float(global_yield_pct), 2),
            'portfolio_items': df[['ticker', 'investment_type', 'total_purchase_value', 'current_value', 'profit_loss']].to_dict(orient='records')
        }

