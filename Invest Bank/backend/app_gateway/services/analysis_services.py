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

    @staticmethod
    def calculate_future_projection(total_assets: float, profile: InvestorProfile, years: int = 1) -> Dict[str, Any]:
        '''Realiza a projeção de crescimento do patrimônio para o futuro.'''
        rate = AnalysisService.PROJECTION_RATES.get(profile, 0.0)
        future_value = total_assets * (1 + rate) ** years
        
        return {
            'initial_assets': round(total_assets, 2),
            'profile': profile,
            'annual_rate': f'{rate * 100}%',
            'time_horizon_years': years,
            'projected_value': round(future_value, 2),
            'estimated_profit': round(future_value - total_assets, 2)
        }
    
    @staticmethod
    def get_portfolio_composition(investments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        '''Dados para o gráfico de Pizza: percentual de alocação por tipo.'''
        df = pd.DataFrame(investments)
        df['investment_type'] = df['asset'].apply(AnalysisService._extract_type)
        df['current_value'] = df['quantity'].astype(float) * df['asset'].apply(AnalysisService._extract_price)
        composition = df.groupby('investment_type')['current_value'].sum().reset_index()
        return composition.to_dict(orient='records')
    
    @staticmethod
    def get_assets_performance(investments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        '''Dados para o gráfico de Barras: lucro ou prejuízo individual por ticker.'''
        df = pd.DataFrame(investments)
        df['ticker'] = df['asset'].apply(AnalysisService._extract_ticker)
        df['total_paid'] = df['quantity'].astype(float) * df['purchase_price'].astype(float)
        df['current_val'] = df['quantity'].astype(float) * df['asset'].apply(AnalysisService._extract_price)
        df['profit_loss'] = df['current_val'] - df['total_paid']
        performance = df.groupby('ticker')['profit_loss'].sum().reset_index()
        return performance.to_dict(orient='records')
    
    @staticmethod
    def get_asset_history_with_events(ticker: str, history_df: pd.DataFrame, user_investments: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Dados para o gráfico de Linha: Preços com marcações de compra.'''
        chart_data = {
            'dates': history_df.index.strftime('%Y-%m-%d').tolist(),
            'prices': history_df['Close'].tolist()
        }
        purchase_events = []
        for inv in user_investments:
            purchase_events.append({
                'date': inv['application_date'][:10],
                'purchase_price': float(inv['purchase_price']),
                'label': f'Comprou {inv['quantity']} unidades'
            })
        return {
            'ticker': ticker,
            'price_history': chart_data,
            'purchase_events': purchase_events
        }
    
    @staticmethod
    def get_highlights(investments: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Identifica o melhor e o pior ativo da carteira.'''
        df = pd.DataFrame(investments)
        df['ticker'] = df['asset'].apply(AnalysisService._extract_ticker)
        df['current_price'] = df['asset'].apply(AnalysisService._extract_price)
        df['profit'] = (df['current_price'] - df['purchase_price'].astype(float)) * df['quantity'].astype(float)
        best_row = df.loc[df['profit'].idxmax()]
        worst_row = df.loc[df['profit'].idxmin()]
        return {
            'best_performer': {'ticker': best_row['ticker'], 'profit': round(best_row['profit'], 2)},
            'worst_performer': {'ticker': worst_row['ticker'], 'profit': round(worst_row['profit'], 2)}
        }
    
    @staticmethod
    def calculate_volatility(history_df: pd.DataFrame) -> float:
        '''Calcula a volatilidade anualizada do ativo.'''
        returns = history_df['Close'].pct_change()
        volatility = returns.std() * np.sqrt(252)
        return round(float(volatility * 100), 2) 
    
    @staticmethod
    def compare_with_benchmark(portfolio_yield_pct: float, benchmark_df: pd.DataFrame) -> Dict[str, Any]:
        '''Compara o rendimento da carteira com o Ibovespa.'''
        if benchmark_df.empty:
            return {'error': 'Dados do Benchmarking indisponíveis'}
        start_price = benchmark_df['Close'].iloc[0]
        end_price = benchmark_df['Close'].iloc[-1]
        market_yield = ((end_price - start_price) / start_price) * 100
        alpha = portfolio_yield_pct - market_yield
        return {
            'benchmark_name': 'Ibovespa (^BVSP)',
            'portfolio_yield': f'{round(portfolio_yield_pct, 2)}%',
            'market_yield': f'{round(market_yield, 2)}%',
            'performance_status': 'ACIMA DA MÉDIA' if alpha > 0 else 'ABAIXO DA MÉDIA',
            'difference_pct': f'{round(abs(alpha), 2)}%'
        }