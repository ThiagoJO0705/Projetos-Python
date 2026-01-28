import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app_gateway.app.dependencies import validate_active_investor
from app_gateway.schemas.schemas import InvestmentCreate, InvestmentUpdate, InvestmentResponse
from app_gateway.services.investments_services import InvestmentDataService
from app_gateway.services.javer_services import JaverService
from app_gateway.services.yfinance_services import YahooService
from app_gateway.services.assets_services import AssetDataService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from app_data.schemas.enums import InvestmentType

security = HTTPBearer()
investments = APIRouter(prefix='/investments', tags=['investments'])

@investments.get('/me', response_model=List[InvestmentResponse])
async def get_my_investments(user: dict = Depends(validate_active_investor)):
    '''Lista todos os investimentos ativos na carteira do usuário logado.'''
    investments = await InvestmentDataService.get_customer_investments(user['pyinvest']['id'])
    usd_rate = YahooService.get_usd_brl_rate()
    for inv in investments:
        ticker = inv['asset']['ticker']
        asset_type = inv['asset']['type']
        currency = inv['asset']['currency']
        quantity = float(inv['quantity'])
        if asset_type == InvestmentType.FIXED_INCOME:
            live_price = 1.0
        else:
            live_price = YahooService.get_current_price(ticker)
        inv['asset']['current_price'] = live_price
        if currency == 'USD':
            inv['current_value_usd'] = round(quantity * live_price, 2)
            inv['current_value_brl'] = round(quantity * live_price * usd_rate, 2)
        else:
            inv['current_value_brl'] = round(quantity * live_price, 2)
            inv['current_value_usd'] = round((quantity * live_price) / usd_rate, 2)
    return investments

@investments.post('/buy')
async def buy_investment(purchase_data: InvestmentCreate, user: dict = Depends(validate_active_investor), auth: HTTPAuthorizationCredentials = Depends(security)):
    '''Efetua a compra de um ativo descontando o saldo do Banco Javer:'''
    ticker = purchase_data.ticker.upper()
    quantity = float(purchase_data.quantity)
    token = auth.credentials
    currency = 'BRL'
    fixed_income_prefixes = ['CDB', 'LCI', 'LCA', 'TESOURO', 'FIXED']
    is_fixed_income = any(ticker.startswith(p) for p in fixed_income_prefixes)
    if is_fixed_income:
        unit_price = 1.00
        asset_market_info = {
            'ticker': ticker,
            'name': f'Investimento Renda Fixa - {ticker}',
            'type': InvestmentType.FIXED_INCOME,
            'currency': 'BRL'
        }
    else:
        asset_market_info = YahooService.get_asset_details(ticker)
        if not asset_market_info:
            raise HTTPException(status_code=404, detail=f'Ativo {ticker} não encontrado no mercado financeiro.')
        unit_price = float(asset_market_info['current_price'])
        currency = asset_market_info['currency'] 
    total_cost = unit_price * quantity
    if currency == 'USD':
        usd_rate = YahooService.get_usd_brl_rate()
        total_cost = total_cost * usd_rate
    user_balance = float(user['javer']['balance'])
    if user_balance < total_cost:
        raise HTTPException(status_code=400, detail=f'Saldo insuficiente no Javer. Custo total: R${total_cost:.2f}, Seu Saldo: R${user_balance:.2f}')
    db_asset = await AssetDataService.get_asset_by_ticker(ticker)
    if not db_asset:
        db_asset = await AssetDataService.create_asset(asset_market_info)
    investment_payload = {
        'customer_id': str(user['pyinvest']['id']),
        'asset_id': str(db_asset['id']),
        'quantity': quantity,
        'purchase_price': unit_price,
        'is_active': True
    }
    new_investment = await InvestmentDataService.create_investment(investment_payload)
    investment_id = new_investment['id']
    try:
        await JaverService.debit_account(token=token, amount=total_cost, ticker=ticker)
    except Exception as e:
        await InvestmentDataService.delete_investment(investment_id)
        raise HTTPException(status_code=500, detail=f'A compra foi cancelada por erro no débito bancário: {str(e)}')
    return {
        'message': 'Compra realizada com sucesso!',
        'total_debited_brl': round(total_cost, 2),
        'investment_details': new_investment
    }

@investments.post('/register', response_model=InvestmentResponse)
async def register_investment(registration_data: InvestmentCreate, user: dict = Depends(validate_active_investor)):
    '''Registra um investimento antigo sem afetar o saldo do Banco Javer.'''
    ticker = registration_data.ticker.upper()
    purchase_price = float(registration_data.purchase_price) if registration_data.purchase_price else 0.0
    purchase_date = registration_data.purchase_date
    if purchase_price <= 0:
        raise HTTPException(status_code=400, detail='O preço deve ser maior que zero.')
    if not purchase_date:
        raise HTTPException(status_code=400, detail='A data da compra é obrigatória para registros.')
    fixed_prefixes = ['CDB', 'LCI', 'LCA', 'TESOURO', 'FIXED']
    if any(ticker.startswith(p) for p in fixed_prefixes):
        asset_market_info = {
            'ticker': ticker, 'name': f'Renda Fixa - {ticker}',
            'type': InvestmentType.FIXED_INCOME, 'currency': 'BRL'
        }
    else:
        day_bounds = YahooService.get_price_on_date(ticker, purchase_date)
        asset_market_info = YahooService.get_asset_details(ticker)
        if not day_bounds:
            raise HTTPException(status_code=400, detail=f'Não há dados de mercado para {ticker} em {purchase_date}. Verifique se foi um final de semana ou feriado.')
        if not (day_bounds['day_low'] * 0.99 <= purchase_price <= day_bounds['day_high'] * 1.01):
            raise HTTPException(status_code=400,
                detail=(
                    f'Preço R${purchase_price} inválido para a data {purchase_date}. '
                    f'Nesse dia, o ativo {ticker} variou entre R${day_bounds['day_low']:.2f} e R${day_bounds['day_high']:.2f}.'
                )
            )
        live_price = YahooService.get_current_price(ticker)
    db_asset = await AssetDataService.get_asset_by_ticker(ticker)
    if not db_asset:
        db_asset = await AssetDataService.create_asset(asset_market_info)
    return await InvestmentDataService.create_investment({
        'customer_id': str(user['pyinvest']['id']),
        'asset_id': str(db_asset['id']),
        'quantity': float(registration_data.quantity),
        'purchase_price': purchase_price,
        'application_date': purchase_date,
        'is_active': True
    })

@investments.patch('/{investment_id}', response_model=InvestmentResponse)
async def update_investment(investment_id: uuid.UUID, update_data: InvestmentUpdate, user: dict = Depends(validate_active_investor), auth: HTTPAuthorizationCredentials = Depends(security)):
    '''Altera dados ou realiza venda de um investimento'''
    current_inv = await InvestmentDataService.get_investment_by_id(investment_id)
    if current_inv['customer_id'] != str(user['pyinvest']['id']):
        raise HTTPException(status_code=403, detail='Acesso negado.')
    current_qty = float(current_inv['quantity'])
    new_qty = float(update_data.quantity) if update_data.quantity is not None else current_qty
    if update_data.is_active is False and new_qty > 0:
        raise HTTPException(status_code=400, detail='Venda as cotas antes de desativar.')
    if new_qty < current_qty:
        sold_qty = current_qty - new_qty
        ticker = current_inv['asset']['ticker']
        currency = current_inv['asset']['currency']
        live_market_price = YahooService.get_current_price(ticker)
        if live_market_price <= 0:
            raise HTTPException(status_code=400, detail='Mercado indisponível para venda no momento.')
        sale_value_original = sold_qty * live_market_price
        if currency == 'USD':
            usd_rate = YahooService.get_usd_brl_rate()
            sale_value_brl = sale_value_original * usd_rate
        else:
            sale_value_brl = sale_value_original
        await JaverService.credit_account(auth.credentials, sale_value_brl)
    update_payload = update_data.model_dump(exclude_unset=True, mode='json')
    if new_qty == 0:
        update_payload['is_active'] = False
    return await InvestmentDataService.update_investment(investment_id, update_payload)

@investments.get('/{investment_id}', response_model=InvestmentResponse)
async def get_investment_detail(investment_id: uuid.UUID, user: dict = Depends(validate_active_investor)):
    '''Retorna os detalhes de um investimento específico.'''
    investment = await InvestmentDataService.get_investment_by_id(investment_id)
    if investment['customer_id'] != str(user['pyinvest']['id']):
        raise HTTPException(status_code=403, detail='Acesso negado.')
    ticker = investment['asset']['ticker']
    investment['asset']['current_price'] = YahooService.get_current_price(ticker)
    return investment