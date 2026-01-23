import uuid
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from app_gateway.services.customers_services import CustomerDataService
from app_gateway.services.investments_services import InvestmentDataService
from app_gateway.services.assets_services import AssetDataService
from app_gateway.services.yfinance_services import YahooService
from app_gateway.services.analysis_services import AnalysisService

analytics = APIRouter(prefix='/analytics', tags=['analytics'])

@analytics.get('/wallet/{customer_id}')
async def get_full_portfolio_analysis(customer_id: uuid.UUID):
    '''Retorna uma análise profunda da carteira do investidor.'''
    customer = await CustomerDataService.get_customer_by_id(customer_id)
    investments = await InvestmentDataService.get_customer_investments(customer_id)
    if not investments:
        raise HTTPException(status_code=404, detail='Nenhum investimento encontrado para este cliente para realizar a análise.')
    portfolio_summary = AnalysisService.get_portfolio_analysis(investments=investments, profile=customer['investor_profile'])
    composition_chart = AnalysisService.get_portfolio_composition(investments)
    performance_chart = AnalysisService.get_assets_performance(investments)
    highlights = AnalysisService.get_highlights(investments)
    return {
        'customer_info': {
            'name': customer['name'],
            'profile': customer['investor_profile']
        },
        'portfolio_summary': portfolio_summary,
        'charts': {
            'allocation_by_type': composition_chart,
            'profit_loss_by_ticker': performance_chart
        },
        'highlights': highlights
    }

@analytics.get('/calculations/projection/{customer_id}')
async def get_wealth_projection(customer_id: uuid.UUID):
    '''Calcula a projeção de patrimônio para 1 ano baseado no perfil do investidor.'''
    customer = await CustomerDataService.get_customer_by_id(customer_id)
    current_assets = float(customer.get('total_assets', 0.0))
    projection = AnalysisService.calculate_future_projection(total_assets=current_assets, profile=customer['investor_profile'], years=1)
    return projection

@analytics.get('/calculations/assets/{customer_id}')
async def get_total_net_worth(customer_id: uuid.UUID):
    '''Calcula o patrimônio total atualizado.'''
    customer = await CustomerDataService.get_customer_by_id(customer_id)
    investments = await InvestmentDataService.get_customer_investments(customer_id)
    portfolio_data = AnalysisService.get_portfolio_analysis(
        investments=investments, 
        profile=customer['investor_profile']
    )
    account_balance = float(customer.get('account_balance', 0.0))
    investments_value = portfolio_data['current_portfolio_value']
    return {
        'customer_id': customer_id,
        'account_balance': account_balance,
        'investments_current_value': investments_value,
        'total_net_worth': round(account_balance + investments_value, 2)
    }

@analytics.get('/analises/mercado/{ticker}')
async def get_market_comparison(ticker: str):
    '''Compara o desempenho de um ativo específico com o Ibovespa e calcula volatilidade.'''
    asset_details = YahooService.get_asset_details(ticker)
    if not asset_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Ticker não encontrado no mercado financeiro.'
        )
    history_df = YahooService.get_historical_data(ticker)
    benchmark_df = YahooService.get_historical_data('^BVSP')
    volatility = AnalysisService.calculate_volatility(history_df)
    daily_variation = YahooService.get_market_variation(ticker)
    comparison = AnalysisService.compare_with_benchmark(
        portfolio_yield_pct=daily_variation, 
        benchmark_df=benchmark_df
    )
    return {
        'asset_info': asset_details,
        'metrics': {
            'daily_variation_pct': f'{daily_variation}%',
            'annualized_volatility': f'{volatility}%'
        },
        'market_benchmark_comparison': comparison
    }