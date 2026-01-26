import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Any
from decimal import Decimal
from app_gateway.app.dependencies import validate_active_investor
from app_gateway.schemas.schemas import InvestmentCreate, InvestmentUpdate, InvestmentResponse
from app_gateway.services.investments_services import InvestmentDataService
from app_gateway.services.javer_services import JaverService
from app_gateway.services.yfinance_services import YahooService
from app_gateway.services.assets_services import AssetDataService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 

security = HTTPBearer()
investments = APIRouter(prefix='/investments', tags=['investments'])

@investments.get('/me', response_model=List[InvestmentResponse])
async def get_my_investments(user_context: dict = Depends(validate_active_investor)):
    '''Lista todos os investimentos ativos na carteira do usuário logado.'''
    customer_id = user_context['pyinvest']['id']
    return await InvestmentDataService.get_customer_investments(customer_id)

@investments.post('/buy')
async def buy_investment(purchase_data: InvestmentCreate, user_context: dict = Depends(validate_active_investor), auth: HTTPAuthorizationCredentials = Depends(security)):
    '''Efetua a compra de um ativo descontando o saldo do Banco Javer:'''
    asset_market_info = YahooService.get_asset_details(purchase_data.ticker)
    if not asset_market_info:
        raise HTTPException(status_code=404, detail="Ativo não encontrado no mercado financeiro.")
    unit_price = asset_market_info['current_price']
    total_cost = float(unit_price) * float(purchase_data.quantity)
    if user_context['javer']['balance'] < total_cost:
        raise HTTPException(status_code=400, detail=f"Saldo insuficiente no Banco Javer. Custo: R${total_cost}, Saldo: R${user_context['javer']['balance']}")
    db_asset = await AssetDataService.get_asset_by_ticker(purchase_data.ticker)
    if not db_asset:
        db_asset = await AssetDataService.create_asset(asset_market_info)
    new_investment = await InvestmentDataService.create_investment({
        "customer_id": str(user_context['pyinvest']['id']),
        "asset_id": str(db_asset['id']),
        "quantity": float(purchase_data.quantity),
        "purchase_price": float(unit_price),
        "is_active": True
    })
    await JaverService.debit_account(token=auth.credentials, amount=total_cost, ticker=purchase_data.ticker)
    return {
        "message": "Compra efetuada com sucesso e saldo debitado.",
        "details": new_investment
    }

@investments.post('/register')
async def register_investments():
    pass

@investments.patch('/{investment_id}')
async def get_my_investments():
    pass

@investments.get('/{investment_id}')
async def get_my_investments():
    pass
