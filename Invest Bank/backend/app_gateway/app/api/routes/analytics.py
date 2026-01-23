import uuid
from fastapi import APIRouter, HTTPException, status, Header
from typing import Dict, Any
from app_gateway.services.customers_services import CustomerDataService
from app_gateway.services.investments_services import InvestmentDataService
from app_gateway.services.javer_services import JaverService
from app_gateway.services.yfinance_services import YahooService
from app_gateway.services.analysis_services import AnalysisService

analytics = APIRouter(prefix='/analytics', tags=['analytics'])

async def get_pyinvest_user(authorization: str):
    '''Valida o token no Javer e busca o usuário no PYInvest.'''
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Token de autenticação ausente ou inválido.')
    token = authorization.split(' ')[1]
    javer_user = await JaverService.get_user_data_from_javer(token)
    pyinvest_user = await CustomerDataService.get_customer_by_filter(cpf=javer_user['cpf'])
    if not pyinvest_user:
        raise HTTPException(status_code=404, detail='Usuário autenticado, mas conta de investimentos não encontrada. Por favor, ative sua conta de investidor.')
    return {'javer': javer_user, 'pyinvest': pyinvest_user}

@analytics.get('/wallet/me')
async def get_my_portfolio_analysis(authorization: str = Header(...)):
    ''' Retorna uma análise profunda da carteira do investidor logado.'''
    user_context = await get_pyinvest_user(authorization)
    customer = user_context['pyinvest']
    investments = await InvestmentDataService.get_customer_investments(customer['id'])
    if not investments:
        return {
            'customer_info': {'name': user_context['javer']['name'], 'profile': customer['investor_profile']},
            'message': 'Você ainda não possui investimentos cadastrados.'
        }
    portfolio_summary = AnalysisService.get_portfolio_analysis(investments=investments, profile=customer['investor_profile'])
    return {
        'customer_info': {
            'name': user_context['javer']['name'],
            'profile': customer['investor_profile']
        },
        'portfolio_summary': portfolio_summary,
        'charts': {
            'allocation_by_type': AnalysisService.get_portfolio_composition(investments),
            'profit_loss_by_ticker': AnalysisService.get_assets_performance(investments)
        },
        'highlights': AnalysisService.get_highlights(investments)
    }

@analytics.get('/calculations/projection/me')
async def get_my_wealth_projection(authorization: str = Header(...)):
    '''Calcula a projeção de patrimônio para 1 ano baseado no perfil e ativos do usuário logado.'''
    user_context = await get_pyinvest_user(authorization)
    customer = user_context['pyinvest']
    current_assets = float(customer.get('total_assets', 0.0))
    projection = AnalysisService.calculate_future_projection(total_assets=current_assets, profile=customer['investor_profile'], years=1)
    return projection

@analytics.get('/calculations/net-worth/me')
async def get_my_total_net_worth(authorization: str = Header(...)):
    '''Calcula o patrimônio total liquido'''
    user_context = await get_pyinvest_user(authorization)
    javer_balance = user_context['javer']['balance']
    customer = user_context['pyinvest']
    investments = await InvestmentDataService.get_customer_investments(customer['id'])
    portfolio_data = AnalysisService.get_portfolio_analysis(investments=investments, profile=customer['investor_profile'])
    current_investments_value = portfolio_data['current_portfolio_value']    
    return {
        'javer_account_balance': javer_balance,
        'pyinvest_portfolio_value': current_investments_value,
        'total_net_worth': round(javer_balance + current_investments_value, 2),
        'currency': 'BRL'
    }

@analytics.get('/market/comparison/{ticker}')
async def get_market_analysis(ticker: str):
    '''Compara o desempenho de um ativo específico com o benchmark do mercado (Ibovespa).'''
    asset_details = YahooService.get_asset_details(ticker)
    if not asset_details:
        raise HTTPException(status_code=404, detail='Ticker não encontrado ou inválido no Yahoo Finance.')
    history_df = YahooService.get_historical_data(ticker)
    benchmark_df = YahooService.get_historical_data('^BVSP')
    return {
        'asset_info': asset_details,
        'metrics': {
            'daily_variation_pct': f'{YahooService.get_market_variation(ticker)}%',
            'annualized_volatility': f'{AnalysisService.calculate_volatility(history_df)}%'
        },
        'market_benchmark_comparison': AnalysisService.compare_with_benchmark(
            portfolio_yield_pct=YahooService.get_market_variation(ticker), 
            benchmark_df=benchmark_df
        )
    }