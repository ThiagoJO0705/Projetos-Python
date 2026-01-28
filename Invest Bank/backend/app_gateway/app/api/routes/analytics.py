import uuid
from fastapi import APIRouter, HTTPException, Depends
from app_gateway.services.customers_services import CustomerDataService
from app_gateway.services.investments_services import InvestmentDataService
from app_gateway.services.yfinance_services import YahooService
from app_gateway.services.analysis_services import AnalysisService
from app_gateway.app.dependencies import validate_active_investor
from app_data.schemas.enums import InvestorProfile, InvestmentType

analytics = APIRouter(prefix='/analytics', tags=['analytics'])

@analytics.get('/wallet/me')
async def get_my_portfolio_analysis(user: dict = Depends(validate_active_investor)):
    ''' Retorna uma análise profunda da carteira do investidor logado.'''
    customer = user['pyinvest']
    javer_data = user['javer']
    usd_quote = YahooService.get_usd_brl_rate()
    investments = await InvestmentDataService.get_customer_investments(customer['id'])
    if not investments:
        return {
            'customer_info': {'name': javer_data['name'], 'profile': customer.get('investor_profile', InvestorProfile.UNDEFINED)},
            'message': 'Você ainda não possui investimentos cadastrados.'
        }
    for inv in investments:
        asset_type = inv['asset']['type']
        ticker = inv['asset']['ticker']
        if asset_type != InvestmentType.FIXED_INCOME:
            inv['asset']['current_price'] = YahooService.get_current_price(ticker)
        else:
            inv['asset']['current_price'] = 1.0
    portfolio_summary = AnalysisService.get_portfolio_analysis(
        investments=investments, 
        profile=customer['investor_profile'], 
        usd_rate=usd_quote
    )
    return {
        'customer_info': {
            'name': javer_data['name'],
            'profile': customer['investor_profile']
        },
        'portfolio_summary': portfolio_summary,
        'charts': {
            'allocation_by_type': AnalysisService.get_portfolio_composition(investments, usd_rate=usd_quote),
            'profit_loss_by_ticker': AnalysisService.get_assets_performance(investments, usd_rate=usd_quote)
        },
        'highlights': AnalysisService.get_highlights(investments, usd_rate=usd_quote)
    }

@analytics.get('/calculations/projection/me')
async def get_my_wealth_projection(user: dict = Depends(validate_active_investor)):
    '''Calcula a projeção de patrimônio para 1 ano baseado no perfil e ativos do usuário logado.'''
    customer = user['pyinvest']
    current_assets = float(customer.get('total_assets', 0.0))
    projection = AnalysisService.calculate_future_projection(total_assets=current_assets, profile=customer['investor_profile'], years=1)
    return projection

@analytics.get('/calculations/net-worth/me')
async def get_my_total_net_worth(user: dict = Depends(validate_active_investor)):
    '''Calcula o patrimônio total liquido'''
    customer = user['pyinvest']
    javer_balance = user['javer']['balance']
    usd_quote = YahooService.get_usd_brl_rate()
    investments = await InvestmentDataService.get_customer_investments(customer['id'])
    for inv in investments:
        if inv['asset']['type'] != InvestmentType.FIXED_INCOME:
            inv['asset']['current_price'] = YahooService.get_current_price(inv['asset']['ticker'])
        else:
            inv['asset']['current_price'] = 1.0
    portfolio_data = AnalysisService.get_portfolio_analysis(investments=investments, profile=customer['investor_profile'], usd_rate=usd_quote)
    current_investments_value = portfolio_data['current_portfolio_value']    
    return {
        'javer_account_balance': javer_balance,
        'pyinvest_portfolio_value': current_investments_value,
        'total_net_worth': round(javer_balance + current_investments_value, 2),
        'currency': 'BRL',
        'usd_rate': usd_quote
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